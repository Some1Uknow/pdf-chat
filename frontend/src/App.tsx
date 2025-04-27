import { useState } from "react";
import {
  FileText,
  MessageSquare,
  Upload,
  Bot,
  ChevronRight,
} from "lucide-react";
import Navbar from "./components/Navbar";
import FeatureCard from "./components/FeatureCard";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />

      <main className="flex-grow">
        <section className="bg-gradient-to-b from-red-600 to-red-800 text-white py-20">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
              Chat with Your PDF Documents
            </h2>
            <p className="text-lg md:text-xl mb-8 max-w-2xl mx-auto">
              Upload your PDFs and get instant answers to your questions using advanced AI
            </p>
            <div className="flex justify-center gap-4">
              <a
                href="/upload"
                className="bg-white text-red-600 px-6 py-3 rounded-lg font-semibold text-lg hover:bg-red-50 transition duration-300 flex items-center"
              >
                <Upload className="w-5 h-5 mr-2" />
                Upload PDF
              </a>
              <a
                href="/chat"
                className="bg-red-700 text-white px-6 py-3 rounded-lg font-semibold text-lg hover:bg-red-800 transition duration-300 flex items-center"
              >
                <MessageSquare className="w-5 h-5 mr-2" />
                Start Chat
              </a>
            </div>
          </div>
        </section>

        <section className="py-16">
          <div className="container mx-auto px-4">
            <h3 className="text-2xl md:text-3xl font-bold text-center mb-12">
              How It Works
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <FeatureCard
                icon={<Upload className="w-12 h-12 text-red-600" />}
                title="1. Upload Your PDF"
                description="Simply upload your PDF document to our secure platform"
              />
              <FeatureCard
                icon={<Bot className="w-12 h-12 text-red-600" />}
                title="2. AI Processing"
                description="Our AI analyzes and understands your document content"
              />
              <FeatureCard
                icon={<MessageSquare className="w-12 h-12 text-red-600" />}
                title="3. Start Chatting"
                description="Ask questions and get instant, accurate answers from your document"
              />
            </div>
          </div>
        </section>

        <section className="bg-red-50 py-16">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h3 className="text-2xl md:text-3xl font-bold mb-6">
                Ready to Get Started?
              </h3>
              <p className="text-lg mb-8">
                Upload your first PDF and experience the power of AI-driven document interaction
              </p>
              <a
                href="/upload"
                className="inline-flex items-center bg-red-600 text-white px-8 py-3 rounded-lg font-semibold text-lg hover:bg-red-700 transition duration-300"
              >
                Try It Now
                <ChevronRight className="w-5 h-5 ml-2" />
              </a>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-gray-900 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">
            &copy; 2024 PDF Chat. Powered by advanced AI technology.
          </p>
        </div>
      </footer>
    </div>
  );
}
