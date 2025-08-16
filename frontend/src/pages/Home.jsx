import {useState, useEffect} from "react";
import api from "../api";
import Notes from "../components/Notes"
import "../styles/Home.css"

function Home() {

    const [notes, setNotes] = useState([]);
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");

    useEffect(() => {
        getNotes();
    }, []); 



    const getNotes = () => {
        api

        .get("/notes/")
        .then((res) => res.data)
        .then((data) => {
            
            setNotes(data)
            console.log("this is res", data)
        })
        .catch((err) => {
            console.error("err", err)
        })
    };

    const createNote = (e) => {
        e.preventDefault();
        api

        .post("/notes/", {content, title})
        .then((res) => {
            if(res.status===201) {
                alert("note was created")
            } else {
                alert("there was an error")
            }
            getNotes();
        })
        .catch((err) => alert(err));
    };

    const deleteNote = (id) => {
        api

        .delete(`/notes/${id}/`)
        .then((res) => {
            if(res.status === 204) {
                alert("note was deleted")
            } else {
                alert("Note failed to delete")
            }
            getNotes();
        })
    };


    return (
        <div>
            <div>
                <h2>Notes</h2>
                {notes.map((note) => (
                    <Notes note={note} onDelete={deleteNote} key={note.id} />
                ))}
            </div>
            <h2>Create a Note</h2>
            <form onSubmit={createNote}>
                <label htmlFor="title">Title:</label>
                <br />
                <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                />
                <label htmlFor="content">Content:</label>
                <br />
                <textarea
                    id="content"
                    name="content"
                    required
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                ></textarea>
                <br />
                <input type="submit" value="Submit"></input>
            </form>
        </div>
    );
}

export default Home