import React from "react";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

const SingleTableBadache = ({ content, missingMask, className }) => {
    console.log('Content:', content);
    console.log('Missing Mask:', missingMask);

    const getCellStyle = (rowIndex, colIndex) => {
        const isMissing = missingMask && missingMask[rowIndex] && missingMask[rowIndex][colIndex];
        console.log(`Cell ${rowIndex},${colIndex} isMissing:`, isMissing);

        if (isMissing) {
            return {
                backgroundColor: 'rgba(52, 152, 219, 0.2)',
                boxShadow: 'inset 0 0 0 1px rgba(52, 152, 219, 0.5)',
            };
        }
        return {};
    };

    if (!content || !content.data || !content.columns) {
        return <div>No data available</div>;
    }

    return (
        <div className="overflow-x-auto">

            <table className={className}>

                <thead className="bg-gray-50">
                    <tr>
                        {content.columns.map((column, index) => (
                            <th key={index} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                {column}
                            </th>
                        ))}
                    </tr>
                </thead>

                <tbody className="bg-white divide-y divide-gray-200">
                    {content.data.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                            {row.map((cell, cellIndex) => (
                                <td
                                    key={cellIndex}
                                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                                    style={getCellStyle(rowIndex, cellIndex)}
                                >
                                    {typeof cell === 'number' ? cell.toFixed(2) : cell}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="mt-4 text-sm text-gray-500 flex items-center gap-2">
                <div className="w-4 h-4" style={{ backgroundColor: 'rgba(52, 152, 219, 0.2)' }}></div>
                <span>Valeurs imputées</span>
            </div>
        </div>
    );
};

export default SingleTableBadache;
