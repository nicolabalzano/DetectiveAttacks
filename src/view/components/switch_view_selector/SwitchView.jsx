import React from "react";
import './swicthView.scss';

const SwitchView = ({ startId }) => {

    function handleChangeView(e){
        // delete last char because it's the number of the radio button
        const id = e.target.id.slice(0, -1);
        const table = document.getElementById(id + '_table');
        const hierarchic = document.getElementById(id + '_hierarchic');
        if (e.target.value === '1'){
            table.classList.add('d-none');
            hierarchic.classList.remove('d-none');
        } else {
            table.classList.remove('d-none');
            hierarchic.classList.add('d-none');
        }
    }

    return (
        <div className="switch">
            <input id={startId + '1'} name={startId} type="radio" value="1" className="switch-input"
                   onClick={(e)=>handleChangeView(e)}/>
            <label htmlFor={startId + '1'} className="switch-label switch-label-y">Hierarchic
                view</label>
            <input id={startId + '2'} name={startId} type="radio" value="2" className="switch-input"
                   onClick={(e)=>handleChangeView(e)}/>
            <label htmlFor={startId + '2'} className="switch-label switch-label-n">Table view</label>
            <span className="switch-selector"></span>
        </div>
    );
}

export default SwitchView;