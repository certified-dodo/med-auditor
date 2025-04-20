import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import { highlightPlugin, HighlightArea, RenderHighlightsProps } from '@react-pdf-viewer/highlight';
import '@react-pdf-viewer/highlight/lib/styles/index.css';
import { useEffect, useRef, useState, useMemo } from 'react';

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

// Add interface for component props
interface HighlighterProps {
    onHighlight?: (highlight: HighlightArea & { index: number }) => void;
}

export function Highlighter({ onHighlight }: HighlighterProps = {}) {
    // Create a reference to store the highlight API
    const viewerRef = useRef(null);
    // Track current active highlight index
    const [activeHighlightIndex, setActiveHighlightIndex] = useState(0);
    const containerRef = useRef<HTMLDivElement>(null);
    // Use a ref to track previous highlight index to prevent infinite loops
    const prevIndexRef = useRef<number>(0);

    const areas = useMemo(() => [
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
    ], []); // Empty dependency array since this data is static

    // Call onHighlight whenever the active highlight changes
    useEffect(() => {
        // Only call the callback if the index has actually changed
        if (onHighlight && prevIndexRef.current !== activeHighlightIndex &&
            activeHighlightIndex >= 0 && activeHighlightIndex < areas.length) {

            onHighlight({
                ...areas[activeHighlightIndex],
                index: activeHighlightIndex
            });

            // Update the previous index ref
            prevIndexRef.current = activeHighlightIndex;
        }
    }, [activeHighlightIndex, areas, onHighlight]);

    // Handle keyboard navigation
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            // Navigate to previous highlight with up or left arrow
            if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
                setActiveHighlightIndex((prevIndex) =>
                    prevIndex === 0 ? areas.length - 1 : prevIndex - 1
                );

                // Jump to the page of the new active highlight
                if (viewerRef.current) {
                    const prevIndex = activeHighlightIndex === 0 ? areas.length - 1 : activeHighlightIndex - 1;
                    const prevHighlight = areas[prevIndex];
                    // Access the jumpToPage method if available
                    // viewerRef.current.jumpToPage(prevHighlight.pageIndex);
                }
            }

            // Navigate to next highlight with enter, down or right arrow
            if (e.key === 'Enter' || e.key === 'ArrowDown' || e.key === 'ArrowRight') {
                setActiveHighlightIndex((prevIndex) => (prevIndex + 1) % areas.length);

                // Jump to the page of the new active highlight
                if (viewerRef.current) {
                    const nextIndex = (activeHighlightIndex + 1) % areas.length;
                    const nextHighlight = areas[nextIndex];
                    // Access the jumpToPage method if available
                    // viewerRef.current.jumpToPage(nextHighlight.pageIndex);
                }
            }
        };

        // Add event listener
        window.addEventListener('keydown', handleKeyDown);

        // Clean up event listener
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [activeHighlightIndex, areas.length]);

    const renderHighlights = (props: RenderHighlightsProps) => (
        <div>
            {areas
                .filter((area) => area.pageIndex === props.pageIndex)
                .map((area, idx) => {
                    // Calculate the absolute index of this highlight in the full areas array
                    const absoluteIndex = areas.findIndex(
                        a => a.pageIndex === props.pageIndex && a.top === area.top && a.left === area.left
                    );
                    const isActive = absoluteIndex === activeHighlightIndex;

                    return (
                        <div
                            key={idx}
                            className={`highlight-area ${isActive ? 'active-highlight' : ''}`}
                            style={Object.assign(
                                {},
                                {
                                    background: isActive ? 'orange' : 'yellow',
                                    opacity: isActive ? 0.6 : 0.4,
                                    outline: isActive ? '2px solid blue' : 'none',
                                },
                                props.getCssProperties(area, props.rotation)
                            )}
                            tabIndex={isActive ? 0 : -1}
                            ref={isActive ? (el) => el && el.focus() : null}
                        />
                    );
                })}
        </div>
    );

    // Create the highlight plugin instance
    const highlightPluginInstance = highlightPlugin({
        renderHighlights,
    });

    return (
        <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
            <div
                className='overflow-auto'
                style={{ height: '100%' }}
                ref={containerRef}
                tabIndex={0} // Make the container focusable
            >
                <Viewer
                    fileUrl="/oasis1-4.pdf"
                    plugins={[highlightPluginInstance]}
                    ref={viewerRef}
                />
            </div>
        </Worker>
    );
}