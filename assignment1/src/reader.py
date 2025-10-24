from typing import Generator



def get_sample(file_path: str) -> Generator[tuple[int, str, int, int, int], None, None]:
    #1::F::1::10::48067
    #UserID::Gender::Age::Occupation::Zip-code
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            content = line.strip()
            if content:  
                parts = content.split("::")
                sample = (int(parts[0]), parts[1], int(parts[2]), int(parts[3]), int(parts[4]))
                yield sample