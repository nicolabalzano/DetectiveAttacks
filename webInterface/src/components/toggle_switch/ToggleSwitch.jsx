import './ToggleSwitch.css';

const ToggleSwitch = ({ checked, onChange, dataOn = "Detected", dataOff = "Not Detected" }) => {
    return (
        <label className="switch">
            <input 
                type="checkbox" 
                checked={checked}
                onChange={onChange}
            />
            <span 
                className="slider" 
                data-on={dataOn}
                data-off={dataOff}
            ></span>
        </label>
    );
};

export default ToggleSwitch;
