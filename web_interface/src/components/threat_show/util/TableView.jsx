import {useEffect} from "react";
import {useState} from "react";
import {useLocation} from "react-router-dom";
import {navigateToThreats} from "../../handle_routing_threats/HandleRoutingThreats";
import('../../../scss/util.scss')

const TableView = ({ infoList, selectedAt, setSelectedAt }) => {

    // store of the color assigned to each source of relationship
    const [colorMapSource, setColorMapSource] = useState({});

    // store of the attack patterns already selected by the user
    const location = useLocation();
    let alreadySelected = location.state ? location.state.alreadySelected : null;


    useEffect(() => {
        const root_element = document.getElementById('root');
        root_element.classList.add('scrollbar')
        if (alreadySelected)
            setSelectedAt(alreadySelected);
            alreadySelected = null;
    }, []);

    function generateRandomColor() {
        const red = Math.floor(Math.random() * 256);
        const green = Math.floor(Math.random() * 256);
        const blue = Math.floor(Math.random() * 256);
        return `rgb(${red}, ${green}, ${blue})`;
    }

    function getColorForSource(source){
        if (source in colorMapSource){
            return colorMapSource[source];
        } else {
            colorMapSource[source] = generateRandomColor();
            setColorMapSource(colorMapSource);
            return colorMapSource[source];
        }
    }

    function formatContentId(content_id) {
        content_id = content_id.replace('.', '\\.');
        content_id = content_id.replace('&', '\\&');
        return content_id;
    }

    function handleSelectedCell(event) {
        const content = event.target;
        const elements = document.querySelectorAll('#' + formatContentId(content.id));

        if (selectedAt && selectedAt.includes(content.id)) {
            setSelectedAt(selectedAt.filter(at => at !== content.id));
            elements.forEach(element => {
                element.classList.remove("bg-primary-opacity");
            });
        }
        else {
            setSelectedAt([...selectedAt, content.id]);
            elements.forEach(element => {
                element.classList.add("bg-primary-opacity");
            });
        }
        console.log(event.target.id);

    }

    useEffect(() => {
        console.log(selectedAt);
    }, [selectedAt]);

    return (
        <div className="row d-flex justify-content-center">
            <div className="mt-3 mb-4  text-center lead">You can select the attack patterns identified through
                your analysis to find out if the attacks you have suffered can be linked to a known Group.
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
                                    style={{background: value, width: '10px', height: '10px'}}
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
                                value.sort((a,b)=> a['ID'].localeCompare(b['ID'])).map((subItem, subIndex) => (
                                    <div
                                        key={subIndex}
                                        className={
                                            (selectedAt.includes(key.replaceAll(' ', '_') + '__' + subItem.ID)
                                                ? 'm-0 border-bottom border-start border-end border-secondary py-2 bg-primary-opacity'
                                                : 'm-0 border-bottom border-start border-end border-secondary py-2')}
                                        style={{fontSize: '12px'}}
                                        id={key.replaceAll(' ', '_') + '__' + subItem.ID}
                                        role="button"
                                        onClick={(e) => handleSelectedCell(e)}
                                    >
                                        {subItem.hasOwnProperty('Attack name') ? subItem['Attack name'] : subItem['Name']}
                                        <p
                                            className="text-decoration-underline link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover m-0"
                                            role="button"
                                            onClick={() => navigateToThreats(subItem['ID'])}
                                        >
                                            {subItem['ID']}
                                        </p>
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
                                ))
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