import RenderDict from "./RenderDict.jsx";

const CardView = ({ infoDict }) => {

    return (
        <div className="border border-2 border-primary rounded p-3 shadow fs-6 ms-5 text-break">
            < RenderDict infoDict={infoDict} />
        </div>
    );
}

export default CardView;