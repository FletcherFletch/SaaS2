import React from "react";
import "../styles/Note.css"

function Note({note, onDelete}) {

    return(
        <div className="note-contianer">
            <p className="note-title">{note.title}</p>
            <p className="note-content">{note.content}</p>
            <button className="delete-button" onClick={() => onDelete(note.id)}>
                delete
            </button>
        </div>
    );
}

export default Note