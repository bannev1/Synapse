import React, { useContext } from 'react'
import { useRouter } from 'next/router'

import '../../styles/view/styles.css'
import { TabContext } from '@/components/TabContext';
import { notFound } from 'next/navigation';
import TabBar from '@/components/TabBar';

function View() {
	const router = useRouter();
	const refTab = router.query.slug;

	const {tabs, setTabs} = useContext(TabContext);

	// Find tab
	var tab = undefined;
	tabs.forEach(tabElem => {
		if (tabElem.name == refTab)
			tab = tabElem
	});

	// Check if tab exists
	if (tab == undefined)
		notFound()

	const graph = tab.graph;

	return (
		<>
			<TabBar currTab={refTab}/>

			<div id="home">
				<div id="toolbar">

				</div>

				<div id="graph">

				</div>

				<div id="miniTools">

				</div>

				<div id="options">

				</div>
			</div>
		</>
	)
}

export default View