'use client'

import { HighlightArea } from "@react-pdf-viewer/highlight";
import { Highlighter } from "./components/highlighter";
import { useState } from "react";

export default function Home() {
  const [highlight, setHighlight] = useState<HighlightArea & { index: number } | null>(null);
  const handleHighlight = (highlight: HighlightArea & { index: number }) => {
    setHighlight({
      ...highlight,
      index: highlight.index
    });
    console.log(highlight);
  }
  return (
    <div className="bg-gradient-to-r from-blue-50 to-white w-full h-full flex flex-col items-center justify-center text-black p-8">
      <p className="text-3xl font-extrabold text-blue-900 mb-6">Medical Auditor</p>
      <div className="flex flex-row w-full max-w-4xl shadow-lg rounded-lg overflow-hidden">
        <div className="w-[40%] h-full bg-white p-4">
          <Highlighter onHighlight={handleHighlight} />
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
