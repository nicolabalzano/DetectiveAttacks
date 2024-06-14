import './file_picker.scss'
import React, { useState } from 'react';
import { uploadReportAPI } from '../api/fetchAPI';


function FilePicker() {
    const [dragActive, setDragActive] = useState(true);
    const [file, setFile] = useState(null);

    const uploadFile = (file_) => {
        const fileName = file_.name;
        const fileExtension = fileName.slice(fileName.lastIndexOf(".") + 1);

        if (!file_) {
            setFile(null);
            const notUploadedElement = document.getElementById('notUploaded');
            notUploadedElement.classList.remove('d-none');
            setTimeout(() => {
                notUploadedElement.classList.add('d-none');
            }, 5000);
        }
        else if (fileExtension != 'pdf' && fileExtension != 'txt') {
            setFile(null);  
            const incorrectExtension = document.getElementById('incorrectExtension');
            incorrectExtension.classList.remove('d-none');
            setTimeout(() => {
                incorrectExtension.classList.add('d-none');
            }, 5000);
        } 
        else {
            setFile(file_);
        }
    }

    const postRequestReportAPI = async () => {
        const uploadError = document.getElementById('uploadError');
        uploadReportAPI(file).then((response) => {
            uploadError.classList.remove('d-none');

            // If the response contains the word 'successfully', the file was uploaded successfully
            // change the text color to green
            if (response.data.includes('successfully')) {
                uploadError.classList.remove('text-danger');
                uploadError.classList.add('text-success');
                setFile(null);
            }

            uploadError.innerHTML = response.data.message;

            // open page of vulnerabilities encountered in the report

            setTimeout(() => {
                uploadError.classList.add('d-none');
            }, 5000);
        }). catch((error) => {
            console.error('Error uploading the file:', error.response || error);
            uploadError.classList.remove('d-none');
            uploadError.innerHTML = "Error uploading the file!";
            setFile(null);
            setTimeout(() => {
                uploadError.classList.add('d-none');
                uploadError.classList.remove('text-success');
                uploadError.classList.add('text-danger')
            }, 5000);
        });
    }

    const handleFileChange = () => {
        const fileInput = document.getElementById('fileInput');
        uploadFile(fileInput.files[0]);
        document.getElementById('fileInput').value = '';
    }

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById('dnd').classList.add('bg-primary-opacity');
    };

    const handleDragIn = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(true);
    };

    const handleDragOut = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        document.getElementById('dnd').classList.remove('bg-primary-opacity');
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        document.getElementById('dnd').classList.remove('bg-primary-opacity');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            uploadFile(e.dataTransfer.files[0]);
        }
    };

        const deleteFile = () => {
            setFile(null);
        }


        return (
            <form className="form-container"
                encType='multipart/form-data'
                onDragOver={handleDrag}
                onDragEnter={handleDragIn}
                onDragLeave={handleDragOut}
                onDrop={handleDrop}>
                <div className="upload-files-container">

                    {/* Drag and drop area */}
                    <div id="dnd" className="drag-file-area justify-content-center text-center">
                        {file
                            ? <div>
                                <span className="material-icons-outlined upload-icon"> file_uploaded </span>
                                <h3 className="dynamic-message"> {file.name} </h3>
                                <span id="deleteFile" role='button' className="btn btn-outline-primary border-0 shadow-none" onClick={(e) => { deleteFile() }}>Delete <i class="bi bi-trash-fill"></i></span>
                            </div>
                            :
                            <div>
                                <span className="material-icons-outlined upload-icon"> file_upload </span>
                                <h3 className="dynamic-message"> Drag & drop any file here </h3>
                                <label className="label">
                                    <p className='m-0'>or</p>
                                    <span className="browse-files">
                                        <input type="file" id='fileInput' className="default-file-input" onChange={(e) => { handleFileChange() }} />
                                        <span className="browse-files-text">browse file </span>
                                        <span>from device</span>
                                    </span>
                                </label>
                            </div>}
                    </div>

                    {/* Error Message */}
                    <span className="text-center">
                        <p id="notUploaded" className='text-danger lead fw-bolder d-none m-0'> Please upload a file first! </p>
                        <p id="incorrectExtension" className='text-danger lead fw-bolder d-none m-0'> Please upload .pdf or .txt file! </p>
                        <p id="uploadError" className='text-danger lead fw-bolder d-none m-0'> Error uploading the file! </p>     
                    </span>
                    <button type="button" className="btn btn-outline-primary mt-3 upload-button fw-semibold shadow" onClick={(e) => { postRequestReportAPI() }}> Upload</button>
                </div>
            </form>
        )

    }
    export default FilePicker;
