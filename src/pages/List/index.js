import React, { useState, useEffect } from 'react';
import api from '../../services/api';

import Container from '../../components/Container';

import './index.css';

export default function List() {
    const [blacklist, setList] = useState([]);
    const [viewableList, setViewableList] = useState([]);

    useEffect(() => {
        const overall_episode = localStorage.getItem('overall_episode');

        api.get(`${overall_episode}`).then((response) => {
            console.log(response.data)
            setList(response.data);
        }).catch(err => {
            console.error(err);
        });

    }, []);

    useEffect(() => {
        (blacklist.length > 0) && numberToArrayOfObjects(184);      // TODO: get number of lowest blacklisterfrom server
    }, [blacklist]);

    function numberToArrayOfObjects(num) {
        let list = [], currentNumber = 0;

        for (let i = 0; i < num; i++) {
            let objAdded = false, allIndexesChecked = false;
            
            if (currentNumber < blacklist.length) {
                let blacklister = blacklist[currentNumber]; 
                
                for (let j = 0; j < blacklister.blacklist_guide.length; j++) {
                    if (blacklister.blacklist_guide[j] === i+1) {
                        list.push({
                            ...blacklister,
                            blacklist_guide: [blacklister.blacklist_guide[j]]
                        });
                        
                        objAdded = true;
                    }
                    if (j === blacklister.blacklist_guide.length - 1) {
                        allIndexesChecked = true;
                    } else if (objAdded) {
                        break;
                    }
                }
            }

            if (!objAdded) {
                list.push({
                    'blacklist_guide': [i+1],
                    'title': ''
                    // 'title': '█'.repeat(getRandomArbitrary(8,15))
                })
            }
            if (objAdded && allIndexesChecked) {
                currentNumber++;
            }
        }

        setViewableList(list);
    }

    function getRandomArbitrary(min, max) {
        return Math.random() * (max - min) + min;
    }

    if (!blacklist) {
        return (
            <Container>
                <h1>Carregando...</h1>
            </Container>
        ) 
    }

    return (
        <Container>
            <h2 className="listTitle">The Blacklist</h2>
            <ul className="blacklist">
                {
                    viewableList.map(blacklister => {
                        return (
                            <li key={blacklister.blacklist_guide[0]}>                               
                                <span className={blacklister.title ? 'red' : ''}>
                                    {`#${blacklister.blacklist_guide[0]}.`.padEnd(6)}
                                </span>
                                <span className={blacklister.title ? '' : 'redacted'}>
                                    {blacklister.title || '⋯'.repeat(getRandomArbitrary(10, 17))}
                                </span>
                            </li>
                        )
                    })
                }
            </ul>
        </Container>
    );
}

// (Array.isArray(blacklist) && blacklist.map(blacklister => {
//     for (let i = 0; i < blacklister.blacklist_guide.length; i++) {
//         while (blacklister.blacklist_guide[i] !== currentNumber) {
//             currentNumber++;
//             console.log(currentNumber)
//             return (
//                 <li key={currentNumber}>
//                     {`${currentNumber} - -------------------------------`}
//                 </li>
//             )
//         }
//         currentNumber++;
//         return (
//             <li key={blacklister.blacklist_guide[i]}>
//                 {`${blacklister.blacklist_guide[i]} - ${blacklister.title}`}
//             </li>
//         )
//     }
    // return (
    //     <li key={blacklister.blacklist_guide[0]}>
    //         {`${blacklister.blacklist_guide[0]} - ${blacklister.title}`}
    //     </li>
    // )
// })) || (error &&
// (<h1>Ops... an error has occurred</h1>))