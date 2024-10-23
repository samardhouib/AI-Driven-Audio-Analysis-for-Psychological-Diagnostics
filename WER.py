import os
from jiwer import wer  # Ensure you have jiwer installed: pip install jiwer

# Path to the folder containing reference transcriptions
reference_folder = r'C:\Users\HP\Desktop\mistral-20240922T134313Z-001\mistral\transcriptions'

# Path to the folder containing your model's generated transcriptions
generated_transcription_folder = r'C:\Users\HP\Desktop\mistral-20240922T134313Z-001\mistral\generated'

def load_transcription(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def calculate_wer(reference_folder, generated_folder):
    total_wer = 0
    count = 0

    # Print the number of files in the reference and generated folders
    print(f"Number of reference files: {len(os.listdir(reference_folder))}")
    print(f"Number of generated files: {len(os.listdir(generated_folder))}")

    for reference_file in os.listdir(reference_folder):
        if reference_file.endswith('.txt'):  # Process only text files
            reference_path = os.path.join(reference_folder, reference_file)
            generated_path = os.path.join(generated_folder, reference_file)

            if os.path.exists(generated_path):
                reference_transcription = load_transcription(reference_path)
                generated_transcription = load_transcription(generated_path)

                if reference_transcription and generated_transcription:
                    # Calculate WER
                    error_rate = wer(reference_transcription, generated_transcription)
                    total_wer += error_rate
                    count += 1
                    print(f"WER for {reference_file}: {error_rate:.4f}")

    if count > 0:
        average_wer = (total_wer / count) * 100  # Convert to percentage
        print(f"\nAverage WER: {average_wer:.2f}%")  # Print WER as a percentage
    else:
        print("No transcriptions found for evaluation.")

if __name__ == '__main__':
    calculate_wer(reference_folder, generated_transcription_folder)

