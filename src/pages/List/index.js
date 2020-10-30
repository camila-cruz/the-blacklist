import React, { useState, useEffect } from 'react';
import axios from 'axios';

import Container from '../../components/Container';

export default function List() {
    const [blacklist, setList] = useState([]);

    useEffect(() => {
        const overall_episode = localStorage.getItem('overall_episode');

        axios.get(process.env.NEXT_PUBLIC_FUNCTIONS_API_URL + `/${overall_episode}`).then((response) =>{
            console.log('Funcionou!')
            setList(response);
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
                        <li>{blacklister}</li>
                    })
                }
            </ul>
        </Container>
    );
}