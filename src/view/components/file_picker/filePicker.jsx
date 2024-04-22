import './file_picker.scss'

function FilePicker() {

    return (
        <form className="form-container" encType='multipart/form-data'>
            <div className="upload-files-container">
                <div className="drag-file-area justify-content-center text-center">
                    <span className="material-icons-outlined upload-icon"> file_upload </span>
                    <h3 className="dynamic-message"> Drag & drop any file here </h3>
                    <label className="label">
                        <p style={{margin:'0'}}>or</p>
                        <span className="browse-files">
					<input type="file" className="default-file-input"/>
					<span className="browse-files-text">browse file </span>
				<span>from device</span>
			</span>
                    </label>
                </div>
                <span className="cannot-upload-message"> <span className="material-icons-outlined">error</span> Please select a file first <span
                    className="material-icons-outlined cancel-alert-button">cancel</span> </span>
                <div className="file-block">
                    <div className="file-info"><span className="material-icons-outlined file-icon">description</span>
                        <span className="file-name"> </span> | <span className="file-size">  </span></div>
                    <span className="material-icons remove-file-icon">delete</span>
                </div>
                <button type="button" className="btn btn-outline-primary mt-3 upload-button fw-semibold"> Upload</button>
            </div>
        </form>
    )

}
export default FilePicker;
