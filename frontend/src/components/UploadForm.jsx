import React, { useState } from "react";

const UploadForm = ({ onUploadComplete }) => {
    const [file, setFile] = useState(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const handleFileChange = (e) => {
        const uploadedFile = e.target.files[0];
        if (uploadedFile && uploadedFile.name.endsWith(".zip")) {
            setFile(uploadedFile);
            setError("");
        } else {
            setError("Please upload a valid .zip file.");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError("No file selected.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        setLoading(true);
        setMessage("");

        try {
            const response = await fetch("http://localhost:5000/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Upload failed. Please try again.");
            }

            const data = await response.json();
            onUploadComplete(data);
            setMessage("Upload successful! Insights generated.");
        } catch (error) {
            setError("Error uploading file. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <h2>Upload Your Sleep Data</h2>
            <form onSubmit={handleSubmit} className="upload-form">
                <label htmlFor="fileInput" className="block mb-2">
                    Select exported Health data (.zip):
                </label>
                <input
                    id="fileInput"
                    type="file"
                    onChange={handleFileChange}
                />
                {error && <p className="text-red-500">{error}</p>}
                {message && <p className="text-green-500">{message}</p>}
                {loading ? (
                    <p>Uploading... Please wait.</p>
                ) : (
                    <button type="submit">Upload</button>
                )}
            </form>
        </div>
    );
};

export default UploadForm;
