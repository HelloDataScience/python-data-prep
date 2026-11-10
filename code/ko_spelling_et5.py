# 한글 맞춤법 교정기
# HuggingFace T5 based j5ng/et5-typos-corrector Model

# 필요한 모듈을 임포트합니다.
import os
import shutil
from transformers import T5ForConditionalGeneration
from transformers import T5Tokenizer
from transformers import T5Config
import torch
import random
import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
    
# 한글 구어체 맞춤법 교정을 위한 언어 모델명을 설정합니다.
model_name = 'j5ng/et5-typos-corrector'

# 트랜스포머 모델을 저장할 폴더를 생성합니다.
download_dir = os.path.join(os.path.expanduser(path='~'), 'Downloads')
model_dir = os.path.join('HuggingFace', model_name.replace('/', '-'))
local_model_dir = os.path.join(download_dir, model_dir)

# 모델을 저장하거나 저장된 모델을 불러와서 초기화합니다.
if not os.path.exists(path=local_model_dir):
    print('모델을 다운로드합니다...')
    
    # T5 기반 언어 모델과 토크나이저를 초기화합니다.
    model = T5ForConditionalGeneration.from_pretrained(
        pretrained_model_name_or_path=model_name, 
        cache_dir=local_model_dir, 
        use_safetensors=True
    )
    
    tokenizer = T5Tokenizer.from_pretrained(
        pretrained_model_name_or_path=model_name, 
        cache_dir=local_model_dir
    )
    
    # 모델을 로컬 폴더에 저장합니다.
    model.save_pretrained(save_directory=local_model_dir)
    tokenizer.save_pretrained(save_directory=local_model_dir)
    print(f'모델을 "{local_model_dir}"에 저장했습니다.')
    
    # 모델을 임시로 저장했던 폴더를 삭제합니다.
    delete_folder = os.path.join(local_model_dir, f'models--{model_name.replace("/", "--")}')
    if os.path.exists(path=delete_folder):
        shutil.rmtree(path=delete_folder)
    
else:
    print('저장된 모델을 불러옵니다...')

    # 직접 내려받은 bin 파일을 safetensors 파일로 저장합니다.
    bin_path = os.path.join(local_model_dir, 'pytorch_model.bin')

    if os.path.exists(path=bin_path):
        config = T5Config.from_pretrained(pretrained_model_name_or_path=local_model_dir)
        model = T5ForConditionalGeneration(config=config)

        state_dict = torch.load(f=bin_path, map_location='cpu')
        model.load_state_dict(state_dict=state_dict)

        model.save_pretrained(save_directory=local_model_dir, safe_serialization=True)
        os.remove(bin_path)
    
    model = T5ForConditionalGeneration.from_pretrained(
        pretrained_model_name_or_path=local_model_dir, 
        use_safetensors=True, 
        local_files_only=True
    )
    
    tokenizer = T5Tokenizer.from_pretrained(
        pretrained_model_name_or_path=local_model_dir
    )

print('모델 로딩을 완료했습니다!')

# 사용 가능한 디바이스를 확인합니다.
# [참고] Apple Silicon(M1/M2/M3)에서는 'cuda' 대신 'mps'를 사용합니다.
if torch.cuda.is_available():
    device = 'cuda'
elif torch.backends.mps.is_available():
    device = 'mps'
else:
    device = 'cpu'

# 모델의 파라미터와 연산을 사용 가능한 디바이스로 설정합니다.
model = model.to(device)

# 모델을 추론 모드로 전환합니다.
# [참고] Dropout 등을 비활성화하여 일관된 추론 결과를 생성합니다.
model.eval()

# 한글 구어체 맞춤법 검사기를 생성합니다.
def et5_typo_corrector(text, seed=1):
    """
    et5-typos-corrector 모델을 사용하여 입력 문장의 맞춤법과 띄어쓰기를 교정합니다.

    Parameters
    ----------
    text : str
        맞춤법과 띄어쓰기를 교정할 입력 문장입니다.
    seed : int, default=1
        난수 생성기의 시드 값입니다.
        추론 결과의 재현성을 높이기 위해 사용합니다.

    Returns
    -------
    str
        맞춤법과 띄어쓰기가 교정된 문장입니다.
    """

    # 난수 시드를 고정합니다.
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    # 프롬프트를 설정합니다.
    prompt = '원본 내용을 보존하면서 맞춤법을 고쳐주세요: '

    # 입력 텍스트를 모델에 입력할 PyTorch 텐서 형식으로 인코딩합니다.
    input_encoding = tokenizer(
        text=prompt + text,
        return_tensors='pt'
    )

    # 모델의 generate 함수를 사용하여 텍스트를 생성합니다.
    # input_ids와 attention_mask를 선택한 디바이스(cpu 또는 gpu)로 옮깁니다.

    # max_new_tokens: 입력 문장을 제외하고 새로 생성할 최대 토큰 수를 설정합니다.
    # [참고] max_length는 입력과 출력을 합친 전체 토큰 수를 의미하므로,
    #       일반적으로는 max_new_tokens를 사용하는 것이 더 직관적입니다.

    # num_beams: Beam Search 기법에서 사용할 빔의 개수를 지정합니다.
    # [참고] Beam Search는 여러 후보 문장 중 가장 확률 높은 문장을 선택합니다.

    # early_stopping: True일 때 최적 문장이 확정되면 Beam Search를 조기에 종료합니다.
    #                 False일 때는 모든 Beam Search 탐색이 종료될 때까지 탐색을 계속합니다.

    # length_penalty: 생성 문장의 길이에 대한 페널티를 설정합니다.
    # [참고] 0.8은 짧은 문장 선호, 1.0은 기본값, 1.2는 긴 문장을 선호합니다.

    # do_sample: False일 때 샘플링을 수행하지 않고 Greedy Search 또는 Beam Search를 사용합니다.
    #            True일 때는 Temperature, top_k, top_p 등을 이용한 확률적 샘플링을 수행합니다.

    # no_repeat_ngram_size: 같은 n-gram을 반복 생성되지 않도록 제한합니다.

    # repetition_penalty: 반복 생성된 토큰에 페널티를 부여합니다.(보통 1.0보다 큰 값 사용)

    # top_k, top_p: 샘플링할 때 후보 토큰의 범위를 제한합니다.
    # [참고] top_k와 top_p 매개변수는 다양성과 창의성을 조절하는 매개변수이며,
    #       do_sample=False일 때는 적용되지 않습니다.
    with torch.inference_mode():
        output_encoding = model.generate(
            input_ids=input_encoding.input_ids.to(device),
            attention_mask=input_encoding.attention_mask.to(device),
            max_new_tokens=30,
            num_beams=5,
            early_stopping=True,
            length_penalty=1.5,
            do_sample=False,
            no_repeat_ngram_size=3,
            repetition_penalty=1.5,
            # top_k=50,
            # top_p=0.95
        )

    # 모델이 생성한 토큰 시퀀스를 사람이 읽을 수 있는 텍스트로 변환합니다.
    # skip_special_tokens = True 옵션은 [PAD], [EOS] 등의 특수 토큰을 제거합니다.
    output_text = tokenizer.decode(
        token_ids=output_encoding[0],
        skip_special_tokens=True
    )

    # 결과 텍스트를 반환합니다.
    return output_text

# 한글 맞춤법 검사기를 실행하는 재귀함수를 생성합니다.
def correct(text, show_process=True):
    
    # 입력 문장의 클래스에 맞게 한글 맞춤법 검사를 실행합니다.
    if isinstance(text, str):
        return et5_typo_corrector(text=text)
    
    elif isinstance(text, pd.Series):
        iterator = tqdm(text) if show_process else text
        return type(text)((correct(text=item, show_process=False) for item in iterator), index=text.index)
    
    elif isinstance(text, (list, tuple, np.ndarray)):
        iterator = tqdm(text) if show_process else text
        return type(text)(correct(text=item, show_process=False) for item in iterator)
    
    else:
        raise TypeError('문자열, 리스트, 튜플, 또는 시리즈를 입력하세요!')
        return None


# End of Document