import React, { useState } from "react";
import "./Search.css";
import Result from "./Result";

/*            {response !== null ? 
                response.choices[0].text : ''}*/

export default function Search() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);

  const updateQuery = (e) => {
    setQuery(e.target.value);
  };

  const getResults = () => {
    fetch(`http://127.0.0.1:5000/search?query=${query}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then((res) => res.json())
      .then((r) => {
        setResponse(r);
      });
  };

  return (
    <>
      <h1 className="header">Dex</h1>
      <div className="result-container">
        <div className="search-box-container">
          <input
            type="text"
            placeholder="Where are my keys..."
            className="search-box"
            value={query}
            onChange={(e) => updateQuery(e)}
            onKeyDown={(e) => (e.key === "Enter" ? getResults() : null)}
          ></input>
          <br></br>
          <button className="search-button" onClick={getResults}>
            →
          </button>
        </div>
        <div className="image-container">
          {response !== null ? (
            <>
              {/* <h3 color="white">{JSON.stringify(response.chat_res)}</h3> */}
              {response.images.map((imgUrl) => {
                return <Result imagePath={imgUrl} />;
              })}
              {response.images.length === 0 ? (
                <h3 color="white">I could not find a {response.query}</h3>
              ) : null}
            </>
          ) : (
            ""
          )}
        </div>
      </div>
    </>
  );
}
