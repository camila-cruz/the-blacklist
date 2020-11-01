import React, { useState, useEffect } from 'react';
// import axios from 'axios';
import api from '../../services/api';

import Container from '../../components/Container';

import './index.css';

export default function List() {
    const [blacklist, setList] = useState([]);
    const [error, setError] = useState(null)

    useEffect(() => {
        const overall_episode = localStorage.getItem('overall_episode');

        // axios.get(process.env.NEXT_PUBLIC_FUNCTIONS_API_URL + `/${overall_episode}`).then((response) =>{
        api.get(`/${overall_episode}`).then((response) =>{
            console.log(response.data)
            setList(response.data);
        }).catch(err => {
            console.error(err);
            setError(err);
        });

    }, []);

    // function sortList(list) {
    //     JSON.sort(function(a, b){
    //         return a.blacklist_guide[0] - b.blacklist_guide[0];
    //     });
    // }

    return (
        <Container>
            <h2 className="listTitle">The list</h2>
            <ul className="blacklist">
                {
                    (Array.isArray(blacklist) && blacklist.map(blacklister => {
                        return (
                            <li key={blacklister.blacklist_guide[0]}>
                                {`${blacklister.blacklist_guide[0]} - ${blacklister.title}`}
                            </li>
                        )
                    })) || (error &&
                    (<h1>Ops... an error has occurred</h1>))
                }
            </ul>
        </Container>
    );
}