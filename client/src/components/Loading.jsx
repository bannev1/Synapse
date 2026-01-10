import React from 'react'


function Loading(dark = false) {
	return (
		<div id="loader" className={dark && 'dark'}></div>
	)
}

export default Loading