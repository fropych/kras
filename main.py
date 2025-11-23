import os
import time
from openai import OpenAI

def translate_file_via_openrouter(model_name: str, input_path: str, output_path: str, api_key: str):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    separator = "-=-=-=-=-"

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_path} не найден.")
        return

    raw_segments = content.split(separator)
    segments_to_translate = [s.strip() for s in raw_segments if s.strip()]
    
    translated_segments = []
    
    print(f"Найдено сегментов для перевода: {len(segments_to_translate)}")

    for i, text in enumerate(segments_to_translate, 1):
        print(f"Перевод сегмента {i}/{len(segments_to_translate)}...")
        
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": "Переведи следующий текст на русский язык. Сохрани технические"
                        "термины, перевод должен быть естественным и точно передавать смысл."
                        f"Верни только перевод, без лишних комментариев:\n\n{text}"
                    }
                ],
                extra_body={"reasoning": {"enabled": True}} 
            )

            translation = response.choices[0].message.content
            translated_segments.append(translation)
            
        except Exception as e:
            error_msg = f"[ОШИБКА ПЕРЕВОДА: {str(e)}]"
            print(error_msg)
            translated_segments.append(error_msg)
        time.sleep(0.5)

    output_content = f"\n\n{separator}\n\n".join(translated_segments)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)


if __name__ == "__main__":
    API_KEY = os.getenv('API_KEY')
    assert API_KEY is not None, 'Вы забыли указать переменную окружения API_KEY'

    models = [
        'openai/gpt-oss-20b:free',
        'x-ai/grok-4.1-fast:free',
        'google/gemma-3n-e2b-it:free',
        
    ]

    for model in models:
        translate_file_via_openrouter(
            model_name=model,  
            input_path="input.txt",
            output_path=f"results/{model.split('/')[-1]}.txt",
            api_key=API_KEY
        )
