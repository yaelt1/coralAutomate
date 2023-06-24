import React, { useState } from 'react';
import axios from 'axios';
import './Daily.css';
function DailyReport() {
    const [excelSheetUrl, setExcelSheetUrl] = useState('');
    const [mail, setmail] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [workMessage, setWorkMessage] = useState('');

    const handleClickMail = async () => {
        if (mail.trim() === '') {
            setErrorMessage('Email field is required');
            return;
        }
        else {
            setErrorMessage('');
            if (excelSheetUrl === null || excelSheetUrl.trim() === '') {
                setErrorMessage('Excel Sheet not generated');
                return;
            }
            else {
                try {
                    const response = await axios.post('http://127.0.0.1:5000/api/send-mail', { "email": mail, "path": excelSheetUrl });
                    alert('Mail Sent');
                }
                catch (error) {
                    console.error('API request error:', error);
                }

            }
        }
    }

    const handleClick = async () => {
        try {
            setWorkMessage("working on the report")
            const response = await axios.post('http://127.0.0.1:5000/api/generate-excel');
            const generatedSheetUrl = response.data.sheetUrl;
            setExcelSheetUrl(generatedSheetUrl);
            alert('Excel Sheet Generated');
            setWorkMessage("");
            console.log(generatedSheetUrl);
        } catch (error) {
            console.error('API request error:', error);
            alert('Failed to generate Excel Sheet');
        }


    };

    const handleDownload = () => {
        if (excelSheetUrl) {
            const link = document.createElement('a');
            link.href = excelSheetUrl;
            link.download = 'ExcelReport.xlsx';
            link.click();
        }
    };


    return (
        <div>
            <p>Click the Button to Genarate and Download a new Status Report</p>
            <div className="button-container">
                <button onClick={handleClick}>Generate Excel Report</button>
                {excelSheetUrl && (
                    <a href={excelSheetUrl} download>
                        <button onClick={handleDownload}>Download Excel Report</button>
                    </a>
                )}
            </div>
            {workMessage && <h1>{workMessage}</h1>}
            <input type="email" placeholder='Enter Email' value={mail} onChange={(e) => setmail(e.target.value)}></input>
            {errorMessage && <h1>{errorMessage}</h1>}
            <button onClick={handleClickMail}>Send Report to Mail</button>
        </div>
    );
}

export default DailyReport;
