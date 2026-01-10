import React from 'react'


function Loading({dark = false, fullScreen = true}) {
	return (
		<div id="loader" className={(dark ? 'dark' : '') + (fullScreen ? 'fullScreen' : '')}>
			<svg viewBox="25 25 50 50"> {/* https://uiverse.io/barisdogansutcu/light-rat-32 */}
				<circle r="20" cy="50" cx="50"></circle>
			</svg>
		</div>
	)
}

export default Loading