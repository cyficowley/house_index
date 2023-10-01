import React from 'react'

export default function Result(props) {
    return (
        <div>
            <img className='result-item' src={props.src} width="200px" height="200px"></img>
        </div>
    )
}
