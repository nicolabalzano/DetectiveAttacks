import { useEffect } from "react";
import { useState } from "react";
import { useLocation } from "react-router-dom";
import { navigateToThreats } from "../../handle_routing_threats/HandleRoutingThreats";
import('../../../scss/util.scss')

const TableView = ({ infoList, selectedAt, setSelectedAt }) => {

    // store of the color assigned to each source of relationship
    const [colorMapSource, setColorMapSource] = useState({});

    // store of the attack patterns already selected by the user
    const location = useLocation();
    let alreadySelected = location.state ? location.state.alreadySelected : null;

    var parentIdForRendering = '*****';

    useEffect(() => {
        const root_element = document.getElementById('root');
        root_element.classList.add('scrollbar')
        if (alreadySelected)
            setSelectedAt(alreadySelected);
        alreadySelected = null;
    }, []);

    function isChild(idChild) {
        if (idChild.includes(parentIdForRendering)) {
            return true;
        }
        parentIdForRendering = idChild;
        return false;
    }
    function nextIdIsParent(idParent, idChild) {
        if (idParent.includes(idChild)) {
            return true;
        }
        return false;
    }

    function generateRandomColor() {
        const red = Math.floor(Math.random() * 256);
        const green = Math.floor(Math.random() * 256);
        const blue = Math.floor(Math.random() * 256);
        return `rgb(${red}, ${green}, ${blue})`;
    }

    function getColorForSource(source) {
        if (source in colorMapSource) {
            return colorMapSource[source];
        } else {
            colorMapSource[source] = generateRandomColor();
            setColorMapSource(colorMapSource);
            return colorMapSource[source];
        }
    }

    function formatContentId(content_id) {
        content_id = content_id.replace(/\./g, '\\.');
        content_id = content_id.replace(/\&/g, '\\&');
        return content_id;
    }

    function handleSelectedCell(contentId) {
        const elements = document.querySelectorAll('#' + formatContentId(contentId));
        console.log(selectedAt);

        if (selectedAt && selectedAt.includes(contentId)) {
            setSelectedAt(selectedAt.filter(at => at !== contentId));
            elements.forEach(element => {
                {/* Avoid to change the color of the caret icon */}
                if(element.tagName !== 'I'){ 
                    element.classList.remove("bg-primary-opacity");
                }
            });
        }
        else {
            setSelectedAt([...selectedAt, contentId]);
            elements.forEach(element => {
                {/* Avoid to change the color of the caret icon */}
                if(element.tagName !== 'I'){
                    element.classList.add("bg-primary-opacity");
                }
            });
        }

    }

    function handleDropdown(event, parentId) {
        const contentId = parentId;
        const allElements = document.querySelectorAll('*');
        let i = event.target.closest('i')

        allElements.forEach(element => {
            if ( !element.id.endsWith(contentId) && element.id.includes(contentId)) {
                if (element.classList.contains('d-none')) {
                    element.classList.remove('d-none');
                    i.classList.remove('bi-caret-down-fill');
                    i.classList.add('bi-caret-up-fill');
                }
                else {
                    element.classList.add('d-none');
                    i.classList.remove('bi-caret-up-fill');
                    i.classList.add('bi-caret-down-fill');
                }
            }
        });
    }

    function isClickedDropdown(dropdown_id) {
        const dropdown = document.getElementById(dropdown_id);

        if (dropdown && dropdown.classList.contains('bi-caret-up-fill')) {
            return true;
        }
        return false;
    }

    useEffect(() => {
    }, [selectedAt]);

    return (
        <div className="row d-flex justify-content-center">
            <div className="mt-3 mb-4 text-center lead">You can select the attack patterns identified through
                your analysis to find out if the attacks you have suffered can be linked to a known Threat Agents/Groups.
            </div>

            {Object.keys(colorMapSource).length > 0 && (
                <>
                    <div className="fw-bold text-secondary">Source of relationship:</div>
                    <div className="mb-3 mt-1">
                        {Object.entries(colorMapSource).map(([key, value]) => (
                            <div key={key} className="d-inline-block justify-content-start">
                                <span
                                    className="m-0 ms-1 ms-4 text-decoration-underline link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover"
                                    role="button"
                                    onClick={() => navigateToThreats(key)}
                                >
                                    {key}
                                </span>
                                <span
                                    className="d-inline-block ms-1"
                                    style={{ background: value, width: '10px', height: '10px' }}
                                ></span>
                            </div>
                        ))}
                    </div>
                </>
            )}

            {Array.isArray(infoList) ? (
                infoList.map((subDict, subIndex) => (
                    Object.entries(subDict).map(([key, value]) => (
                        <div key={key} className="col p-0 text-center text-break">
                            <p className="m-0 py-2 border border-secondary">
                                <span className="fw-semibold fs-6">{key}</span>
                            </p>
                            {Array.isArray(value) ? (
                                value.sort((a, b) => a['ID'].localeCompare(b['ID'])).map((subItem, subIndex) => {

                                    {/* If the attack pattern is a child, hidden that to show when client click on caret down */}
                                    const isChildPattern=isChild(subItem['ID'])
                                    var classesForChild='ms-0'
                                    if(isChildPattern && isClickedDropdown(key + '_' + parentIdForRendering)){
                                        classesForChild='ms-3'
                                    }
                                    else if (isChildPattern && !selectedAt.includes(key.replaceAll(' ', '_') + '__' + subItem.ID)){
                                        classesForChild='ms-3 d-none'
                                    }           
                                    else if(isChildPattern){
                                        classesForChild='ms-3'
                                    }

                                    return (
                                    <div
                                        key={subIndex}
                                        className={
                                            (selectedAt.includes(key.replaceAll(' ', '_') + '__' + subItem.ID)
                                                ? 'm-0 border-bottom border-top border-start border-end border-secondary bg-primary-opacity d-flex align-items-center py-2'
                                                : 'm-0 border-bottom border-top border-start border-end border-secondary d-flex align-items-center py-2') + ' ' + classesForChild}
                                        style={{ fontSize: '12px' }}
                                        id={key.replaceAll(' ', '_') + '__' + subItem.ID}
                                    >
                                        <div 
                                            style={{ flex: '90%' }} 
                                            role="button"
                                            onClick={(e) => handleSelectedCell(key.replaceAll(' ', '_') + '__' + subItem.ID)}
                                        > 
                                            <div onClick={(e) => { e.currentTarget.parentNode.click() }}> {/* Click on the row perform click on parent to select cell*/}
                                                {subItem.hasOwnProperty('Attack name') ? subItem['Attack name'] : subItem['Name']}
                                            </div>
                                            <p
                                                className="text-decoration-underline link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover m-0"
                                                role="button"
                                                onClick={() => navigateToThreats(subItem['ID'])}
                                            >
                                                {subItem['ID']}
                                            </p>

                                            {/* If there is a relationship, put a color for that */}
                                            <div className="d-flex justify-content-end me-1">
                                                {subItem.hasOwnProperty('Relationship Source ID') && (
                                                    <div
                                                        style={{
                                                            background: getColorForSource(subItem['Relationship Source ID']),
                                                            width: '10px',
                                                            height: '10px'
                                                        }}
                                                    ></div>
                                                )}
                                            </div>
                                        </div>
                                        
                                        {/* Exapand attack patterns for child */}
                                        {
                                            !isChildPattern && value.length-1 > subIndex && nextIdIsParent(value[subIndex+1]['ID'], subItem['ID'] ) && (
                                                <div style={{ flex: '10%' }}>
                                                    <i 
                                                        id={key + '_' + parentIdForRendering} 
                                                        className="bi bi-caret-down-fill text-secondary" 
                                                        role="button"
                                                        onClick={(e)=>{handleDropdown(e, key.replaceAll(' ', '_') + '__' + subItem.ID)}}></i>
                                                </div>
                                            )
                                        }
                                    </div>
                                    )
                                })
                            ) : null}
                        </div>
                    ))
                ))
            ) : null
            }
        </div>
    );

}

export default TableView;