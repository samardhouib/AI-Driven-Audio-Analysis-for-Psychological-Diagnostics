from flask import Flask, render_template, request, jsonify, send_file, url_for
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import io
from datetime import datetime
from transcription import AudioTranscriber
from summary_generation import MedicalSummaryGenerator
from pdf_generation import PDFGenerator

app = Flask(__name__)

recording = False
audio_data = None
taux_echantillonnage = 50000  # Fréquence d'échantillonnage en Hz
hf_token = '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'  # Hugging Face Token


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start-recording', methods=['POST'])
def start_recording():
    global audio_data, recording
    duree = int(request.form.get('duree', 5))  # Récupère la durée depuis le formulaire
    audio_data = sd.rec(int(duree * taux_echantillonnage), samplerate=taux_echantillonnage, channels=2, dtype='int16')
    recording = True
    return jsonify({"status": "Recording started"})


@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    global audio_data, recording
    if recording:
        sd.stop()  # Arrêter l'enregistrement en cours
        recording = False
        return jsonify({"status": "Recording stopped"})
    return jsonify({"status": "No recording in progress"}), 400


@app.route('/save-recording', methods=['POST'])
def save_recording():
    global audio_data, taux_echantillonnage
    if audio_data is not None:
        # Path to save the recorded audio
        audio_path = 'recorded_audio.mp3'

        # Convertir le tableau numpy en audio WAV en mémoire
        wav_segment = AudioSegment(
            data=np.array(audio_data, dtype=np.int16).tobytes(),
            sample_width=2,
            frame_rate=taux_echantillonnage,
            channels=2
        )

        # Sauvegarder en MP3 dans un fichier
        wav_segment.export(audio_path, format='mp3')

        # Transcribe audio
        transcriber = AudioTranscriber()
        transcription = transcriber.transcribe_audio(audio_path)

        # Generate medical summary
        summary_generator = MedicalSummaryGenerator(token=hf_token)
        medical_summary = summary_generator.get_medical_summary(transcription)

        # Extract summary parts
        extracted_summary = summary_generator.extract_summary_parts(medical_summary)

        # Generate PDF
        pdf_filename = 'medical_summary.pdf'
        pdf_generator = PDFGenerator()
        pdf_generator.generate_pdf(extracted_summary, pdf_filename)

        # Return the PDF file path
        return jsonify({"status": "Recording saved", "pdf_url": url_for('download_pdf', filename=pdf_filename)})

    return jsonify({"status": "No recording available"}), 400


@app.route('/download-pdf/<filename>', methods=['GET'])
def download_pdf(filename):
    return send_file(filename, as_attachment=False)


if __name__ == '__main__':
    app.run(debug=True)
