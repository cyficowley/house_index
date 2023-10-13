import React from "react";

export default function Result(props) {
  return (
    <div>
      <img className="result-item" src={props.imagePath} width="400px" height="400px"></img>
    </div>
  );
}
