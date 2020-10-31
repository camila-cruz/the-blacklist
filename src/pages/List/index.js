import React, { useState, useEffect } from 'react';
import axios from 'axios';
import api from '../../services/api';

import Container from '../../components/Container';

export default function List() {
    const [blacklist, setList] = useState([]);

    useEffect(() => {
        const overall_episode = localStorage.getItem('overall_episode');

        // axios.get(process.env.NEXT_PUBLIC_FUNCTIONS_API_URL + `/${overall_episode}`).then((response) =>{
        api.get(`${overall_episode}`).then((response) =>{
            console.log(response.data)
            setList(response.data);
        });

    }, []);

    // function sortList() {
    //     JSON.sort(function(a, b){
    //         return a.blacklist_guide[0] - b.blacklist_guide[0];
    //     });
    // }

    return (
        <Container>
            <h2>The list</h2>
            <ul>
                {
                    blacklist.map(blacklister => {
                        return (
                            <li key={blacklister.blacklist_guide[0]}>
                                {blacklister.title}
                            </li>
                        )
                    })
                }
            </ul>
        </Container>
    );
}