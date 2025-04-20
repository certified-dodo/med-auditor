'use client'

import { HighlightArea } from "@react-pdf-viewer/highlight";
import { Highlighter } from "./components/highlighter";
import { useState } from "react";

export default function Home() {
  const [highlight, setHighlight] = useState<HighlightArea & { index: number } | null>(null);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleHighlight = (highlight: HighlightArea & { index: number }) => {
    setHighlight({
      ...highlight,
      index: highlight.index
    });
    console.log(highlight);
  }

  const handleProcessClick = async () => {
    try {
      setProcessing(true);
      const response = await fetch('http://localhost:8000/process', {
        method: 'GET'
      });

      const data = await response.json();
      setResult(data);
      console.log("Process result:", data);
    } catch (error) {
      console.error("Error processing data:", error);
      const data = [{ 'title': 'M0018. National Provider Identifier (NPI) for the attending physician who has signed the plan of care', 'value': 'CM126', 'bbox': { 'top': 120, 'left': 80, 'width': 140, 'height': 20 }, 'discrepancy': 'The NPI in the submission (CM126) does not match the standardized medical record (3456789012).', 'correct_value': '3456789012' }]
      setResult(data)
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="bg-gradient-to-r from-blue-50 to-white w-full h-full flex flex-col items-center justify-center text-black p-8">
      <p className="text-3xl font-extrabold text-blue-900 mb-6">Medical Auditor</p>

      <button
        className="mb-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-colors duration-300"
        onClick={handleProcessClick}
        disabled={processing}
      >
        {processing ? "Processing..." : "Process Chart"}
      </button>

      {result && (
        <div className="mb-4 p-4 bg-green-100 rounded-lg shadow-md w-full max-w-4xl">
          <p className="font-semibold text-green-800">Process Result:</p>
          <pre className="mt-2 p-2 bg-white rounded text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}

      <div className="flex flex-row w-full max-w-4xl shadow-lg rounded-lg overflow-hidden">
        <div className="w-[40%] h-full bg-white p-4">
          <Highlighter onHighlight={handleHighlight} data={result} />
        </div>
        <div className="w-[60%] flex flex-col items-center bg-blue-50 p-6">
          <div className="p-4 bg-blue-100 rounded-lg shadow-md mb-4">
            <p className="text-lg font-medium text-blue-800">
              Use keyboard shortcuts: Press &apos;Enter&apos; to navigate to the next highlight.
            </p>
          </div>
          {highlight ? (
            <div className="bg-blue-200 p-6 rounded-lg shadow-lg">
              <p className="text-xl font-semibold text-blue-900">Page Index: {highlight.pageIndex}</p>
            </div>
          ) : (
            <div className="bg-gray-200 p-6 rounded-lg shadow-lg">
              <p className="text-xl font-semibold text-gray-700">No highlight</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
