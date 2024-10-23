from transcription import AudioTranscriber
from summary_generation import MedicalSummaryGenerator
from pdf_generation import PDFGenerator
import requests
from time import sleep  # Correct import for sleep function


def main():
    save_url = "http://localhost:5000/save-recording"

    # Wait for a few seconds before sending the request
    wait_time = 10  # Time in seconds
    print(f"Waiting for {wait_time} seconds before saving the recording...")
    sleep(wait_time)  # Use the correct sleep function

    # Request to save the recorded audio
    response = requests.post(save_url)

    if response.status_code == 200:
        audio_path = response.json().get("audio_path")
        if not audio_path:
            print("Error: No audio path received from the server.")
            return

        print(f"Audio saved as: {audio_path}")
        output_pdf = "medical_summary.pdf"
        hf_token = "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"

        # Step 1: Transcribe the audio
        transcriber = AudioTranscriber()
        transcription = transcriber.transcribe_audio(audio_path)

        # Step 2: Generate the medical summary
        summary_generator = MedicalSummaryGenerator(token=hf_token)
        medical_summary = summary_generator.get_medical_summary(transcription)

        # Step 3: Extract summary parts
        extracted_summary = summary_generator.extract_summary_parts(medical_summary)

        print("Extracted Summary:")
        print(extracted_summary)

        # Step 4: Generate the PDF
        pdf_generator = PDFGenerator()
        pdf_generator.generate_pdf(extracted_summary, output_pdf)

    else:
        print("Failed to save recording.Status code:", response.status_code)


if __name__ == "__main__":
    main()
