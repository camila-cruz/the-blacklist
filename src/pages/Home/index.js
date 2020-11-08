import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

import Container from '../../components/Container';

import './index.css';

export default function Home() {
    // Replace it w/ a call to the API
    const seasons = 7;
    const episodes_per_season = [22, 22, 23, 22, 22, 22, 19]
    const [seasonPicked, setSeason] = useState(null)
    const [episodePicked, setEpisode] = useState(null);
    const history = useHistory();

    function numberToArray(num) {
        return Array.from({length: num}, (_, i) => i + 1)
    }

    function showEpisodes(season) {
        setSeason(season - 1);
    }

    function handleEpisodes() {
        // Uses the user's choice to find the overall number of the episode to be passed to the next page

        let overall_episode = episodePicked;

        episodes_per_season.forEach((value, index) => {
            if (index < seasonPicked) {
                overall_episode += value
            }
        })
        
        localStorage.setItem('overall_episode', overall_episode);
        history.push('/list');
    }

    return (
        <Container>
            <h1 className="mainTitle">The Blacklist: The List</h1>
            <p className="mainText">
                In 2013, the notorius criminal Raymond Reddington turns himself in to the FBI. He asks to speak only
                with Elizabeth Keen, a rookie profiler who is barely waking up for her first day in her new office. 
                He proposes a deal, in which he gains immunity and in return provides a list of criminals the bureau 
                doesn't even know they exist. But what list is this?
            </p>
            
            <p className="actionText">Select season and episode for a spoiler free experience:</p>
            <ul className="nonSpoilerList">
                {numberToArray(seasons).map(season => 
                    <li 
                        key={season}
                        onClick={(evt) => showEpisodes(season)}
                        className={season === seasonPicked + 1 ? 'active' : ''}
                    >
                        {season}
                    </li>
                )}
            </ul>
            <br />
            <ul className="nonSpoilerList">
                {numberToArray(episodes_per_season[seasonPicked]).map(episode => 
                    <li 
                        key={episode} 
                        onClick={() => setEpisode(episode)}
                        className={episode === episodePicked ? 'active' : ''}
                    >
                        {episode}
                    </li>
                )}
            </ul>
            {
                episodePicked != null && 
                <div className="callToAction">
                    <button className="continueButton" onClick={handleEpisodes}>CONTINUE</button>
                </div>
            }
        </Container>
    )
}