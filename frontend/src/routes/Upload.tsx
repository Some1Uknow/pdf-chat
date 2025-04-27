import { useState, useCallback } from "react";
import { Upload as UploadIcon, FileText, X, Check, Loader2 } from "lucide-react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const navigate = useNavigate();

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile?.type === "application/pdf") {
      setFile(droppedFile);
    } else {
      toast.error("Please upload a PDF file");
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile?.type === "application/pdf") {
      setFile(selectedFile);
    } else {
      toast.error("Please upload a PDF file");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      toast.success("PDF uploaded successfully!");
      navigate("/chat");
    } catch (error) {
      toast.error("Failed to upload PDF. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Upload Your PDF</h2>
          <p className="mt-2 text-gray-600">
            Upload your PDF document to start chatting with its contents
          </p>
        </div>

        <div
          className={`relative border-2 border-dashed rounded-lg p-12 text-center ${
            isDragging
              ? "border-red-500 bg-red-50"
              : file
              ? "border-red-500 bg-white"
              : "border-gray-300 bg-white hover:border-red-500 transition-colors"
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {file ? (
            <div className="space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <FileText className="w-8 h-8 text-red-500" />
                <span className="text-gray-900 font-medium">{file.name}</span>
                <button
                  onClick={() => setFile(null)}
                  className="p-1 hover:bg-gray-100 rounded-full"
                >
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>
              <button
                onClick={handleUpload}
                disabled={isUploading}
                className="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <Check className="w-5 h-5 mr-2" />
                    Upload PDF
                  </>
                )}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex justify-center">
                <UploadIcon className="w-12 h-12 text-red-500" />
              </div>
              <div className="space-y-1">
                <p className="text-gray-900 font-medium">
                  Drop your PDF here, or{" "}
                  <label className="text-red-600 hover:text-red-700 cursor-pointer">
                    browse
                    <input
                      type="file"
                      className="hidden"
                      accept=".pdf"
                      onChange={handleFileChange}
                    />
                  </label>
                </p>
                <p className="text-gray-500 text-sm">PDF files up to 10MB</p>
              </div>
            </div>
          )}
        </div>

        <div className="mt-8">
          <div className="rounded-lg bg-white shadow-sm">
            <div className="p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Before you upload
              </h3>
              <ul className="space-y-3 text-sm text-gray-600">
                <li className="flex items-center">
                  <Check className="w-5 h-5 text-red-500 mr-2" />
                  Make sure your PDF is text-searchable
                </li>
                <li className="flex items-center">
                  <Check className="w-5 h-5 text-red-500 mr-2" />
                  Files should be less than 10MB
                </li>
                <li className="flex items-center">
                  <Check className="w-5 h-5 text-red-500 mr-2" />
                  For best results, upload documents with clear text content
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
