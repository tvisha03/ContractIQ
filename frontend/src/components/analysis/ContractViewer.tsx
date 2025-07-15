import React, { useMemo } from 'react';
import { PainPoint, Entity } from '../../types/contract';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';

interface ContractViewerProps {
  contractText: string;
  painPoints: PainPoint[];
  entities: Entity[];
  selectedPainPoint?: string;
}

export const ContractViewer: React.FC<ContractViewerProps> = ({
  contractText,
  painPoints,
  entities,
  selectedPainPoint
}) => {
  const highlightedText = useMemo(() => {
    if (!contractText) return '';

    // Collect all highlight ranges (pain points and entities)
    type Highlight = { start: number; end: number; type: string; id: string; className: string };
    const highlights: Highlight[] = [];

    painPoints?.forEach((point, idx) => {
      if (
        typeof point.start === 'number' &&
        typeof point.end === 'number' &&
        point.start >= 0 &&
        point.end > point.start &&
        point.end <= contractText.length &&
        point.end - point.start < contractText.length // prevent full-text highlight
      ) {
        let riskClass = '';
        if ('risk_score' in point && typeof point.risk_score === 'number') {
          const score = point.risk_score as number;
          if (score >= 70) riskClass = 'pain-point-high';
          else if (score >= 50) riskClass = 'pain-point-medium';
          else riskClass = 'pain-point-low';
        } else {
          if (point.type === 'high_risk') riskClass = 'pain-point-high';
          else if (point.type === 'medium_risk') riskClass = 'pain-point-medium';
          else riskClass = 'pain-point-low';
        }
        highlights.push({
          start: point.start,
          end: point.end,
          type: 'painpoint',
          id: String(idx),
          className: `pain-point ${riskClass} ${selectedPainPoint === String(idx) ? 'pain-point-selected' : ''}`
        });
      }
    });

    entities?.forEach((entity, idx) => {
      // @ts-expect-error: start/end may not exist on entity
      if (typeof entity.start === 'number' && typeof entity.end === 'number' && entity.start >= 0 && entity.end > entity.start && entity.end <= contractText.length) {
        highlights.push({
          // @ts-expect-error: start/end may not exist on entity
          start: entity.start,
          // @ts-expect-error: start/end may not exist on entity
          end: entity.end,
          type: 'entity',
          id: String(idx),
          className: `entity entity-${entity.label}`
        });
      }
    });

    // Remove highlights that are duplicates or overlap exactly
    const uniqueHighlights = highlights.filter((h, i, arr) =>
      arr.findIndex(x => x.start === h.start && x.end === h.end && x.type === h.type) === i
    );

    // Split text into segments based on highlight boundaries
    const boundaries = new Set<number>([0, contractText.length]);
    uniqueHighlights.forEach(h => { boundaries.add(h.start); boundaries.add(h.end); });
    const sortedBoundaries = Array.from(boundaries).sort((a, b) => a - b);

    // For each segment, check if it should be highlighted
    let html = '';
    for (let i = 0; i < sortedBoundaries.length - 1; i++) {
      const segStart = sortedBoundaries[i];
      const segEnd = sortedBoundaries[i + 1];
      if (segStart === segEnd) continue;
      const segment = contractText.slice(segStart, segEnd);
      // Find all highlights covering this segment
      const covering = uniqueHighlights.filter(h => h.start <= segStart && h.end >= segEnd);
      if (covering.length > 0) {
        // If multiple, prefer painpoint over entity, and high over medium
        const best = covering.sort((a, b) => {
          if (a.type === 'painpoint' && b.type !== 'painpoint') return -1;
          if (a.type !== 'painpoint' && b.type === 'painpoint') return 1;
          if (a.className.includes('pain-point-high') && !b.className.includes('pain-point-high')) return -1;
          if (!a.className.includes('pain-point-high') && b.className.includes('pain-point-high')) return 1;
          if (a.className.includes('pain-point-medium') && !b.className.includes('pain-point-medium')) return -1;
          if (!a.className.includes('pain-point-medium') && b.className.includes('pain-point-medium')) return 1;
          return 0;
        })[0];
        // Tooltip
        let tooltipText = '';
        if (best.type === 'painpoint') {
          const idx = parseInt(best.id, 10);
          const p = painPoints?.[idx];
          tooltipText = p ? `${p.type}: ${p.issue}` : '';
        } else if (best.type === 'entity') {
          const idx = parseInt(best.id, 10);
          const e = entities?.[idx];
          tooltipText = e ? `${e.label}` : '';
        }
        html += `<mark class="${best.className}" data-id="${best.id}" data-type="${best.type}" title="${tooltipText}">${segment}</mark>`;
      } else {
        html += segment;
      }
    }
    return html;
  }, [contractText, painPoints, entities, selectedPainPoint]);

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Contract Document</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-96 overflow-y-auto bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
          <pre 
            className="whitespace-pre-wrap text-sm leading-relaxed text-gray-900 dark:text-gray-100 font-mono"
            dangerouslySetInnerHTML={{ __html: highlightedText }}
          />
        </div>
      </CardContent>
    </Card>
  );
};