import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import { highlightPlugin, HighlightArea, RenderHighlightsProps } from '@react-pdf-viewer/highlight';
import '@react-pdf-viewer/highlight/lib/styles/index.css';
import { useEffect, useRef } from 'react';

interface Note {
    // The generated unique identifier
    id: number;
    // The note content
    content: string;
    // The list of highlight areas
    highlightAreas: HighlightArea[];
    // The selected text
    quote: string;
}

export function Highlighter() {
    // Create a reference to store the highlight API
    const viewerRef = useRef(null);

    const areas =
        [
            {
                pageIndex: 0,
                height: 1.55401,
                width: 28.1674,
                left: 27.5399,
                top: 15.0772,
            },
            {
                pageIndex: 1,
                height: 1.32637,
                width: 37.477,
                left: 55.7062,
                top: 15.2715,
            },
            {
                pageIndex: 2,
                height: 1.55401,
                width: 28.7437,
                left: 16.3638,
                top: 16.6616,
            },
        ]
    const renderHighlights = (props: RenderHighlightsProps) => (
        <div>
            {areas
                .filter((area) => area.pageIndex === props.pageIndex)
                .map((area, idx) => (
                    <div
                        key={idx}
                        className="highlight-area"
                        style={Object.assign(
                            {},
                            {
                                background: 'yellow',
                                opacity: 0.4,
                            },
                            // Calculate the position
                            // to make the highlight area displayed at the desired position
                            // when users zoom or rotate the document
                            props.getCssProperties(area, props.rotation)
                        )}
                    />
                ))}
        </div>
    );

    // Get the highlight API from the plugin instance


    // Create the highlight plugin instance
    const highlightPluginInstance = highlightPlugin({
        renderHighlights,
        renderHighlightTarget: (props) => {
            return <div>
                <div>
                    {props.highlightAreas.map((area) => <div key={area.pageIndex}>{area.pageIndex}</div>)}
                </div>
            </div>
        }
    });
    return (
        <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
            <div style={{ height: '100%' }}>
                <Viewer
                    fileUrl="/oasis1-4.pdf"
                    plugins={[highlightPluginInstance]}
                    ref={viewerRef}
                />
            </div>
        </Worker>
    );
}