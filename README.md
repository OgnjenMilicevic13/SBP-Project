# SBP-Project

**Pitanje 1:** Koji je prosečan broj značajnih udaraca po borbi za sve borce koji imaju bar jednu borbu u prethodnih 10 godina? 
- Pre optimizacije: *01:28.147*

```js
db.getCollection("stats").aggregate([
    {
        $lookup: {
            from: 'fights',
            localField: 'fight_id',
            foreignField: 'fight_id',
            as: 'fight_info'
        }
    },
    {
        $match: {
            'fight_info.date': {
                $gte: new Date(new Date().setFullYear(new Date().getFullYear() - 10))
            }
        }
    },
    {
        $group: {
            _id: '$fighter_name',
            avg_sig_strikes_landed: {
                $avg: '$sig_strikes_landed'
            },
        }
    }
])
```
![upit1](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit1.png)
![upit1_graph](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit1_graph.png)

- Posle optimizacije: *00:00:241*

```js
db.stats_optimized.aggregate([
    {
        $match: {
            'fight_info.date': {
                $gte: new Date(new Date().setFullYear(new Date().getFullYear() - 10))
            }
        }
    },
    {
        $group: {
            _id: '$fighter_name',
            avg_sig_strikes_landed: {
                $avg: '$sig_strikes_landed'
            },
        }
    }
])
```
![upit1_optimized](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit1_optimized.png)

---

**Pitanje 2:** Koliko pobeda i ukupno borbi imaju borci sa barem jednom pobedom i koji im je odnos pobeda i poraza? 
- Pre optimizacije: *00:07:831*

```js
db.fighters.aggregate([
    {
        $lookup: {
            from: 'fights',
            localField: 'fighter',
            foreignField: 'fighter_name',
            as: 'fights_info'
        }
    },
    {
        $match: {
            'fights_info': {
                $elemMatch: {
                    result: 1
                }
            }
        }
    },
    {
        $addFields: {
            "wins": {
                $size: {
                    $filter: {
                        input: "$fights_info",
                        as: "fight",
                        cond: { $eq: ["$$fight.result", 1] }
                    }
                }
            },
            "total_fights": {
                $size: '$fights_info'
            }
        }
    },
    {
        $addFields: {
            "win/loss_ratio": {
                $divide: ["$wins", "$total_fights"]
            }
        }
    },
    {
        $project: {
            fighter: 1,
            wins: 1,
            total_fights: 1,
            'win/loss_ratio': 1
        }
    }
])
```
![upit2](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit2.png)
![upit2_graph](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit2_graph.png)

- Posle optimizacije: *00:00.006*

```js
db.fighters_optimized.aggregate([
    {
        $match: {
            wins: {
                $gt: 0
            }
        }
    },
    {
        $addFields: {
            "win/loss_ratio": {
                $divide: ["$wins", "$total_fights"]
            }
        }
    },
    {
        $project: {
            fighter: 1,
            wins: 1,
            total_fights: 1,
            'win/loss_ratio': 1
        }
    }
])
```
![upit2_optimized](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit2_optimized.png)

---

**Pitanje 3**: Koje je prosečno vreme trajanja (u sekundama) borbi koje je sudio Herb Dean?
- Pre optimizacije: *01:46.243*

```js
db.getCollection("stats").aggregate([
    {
        $lookup: {
            from: 'fights',
            localField: 'fight_id',
            foreignField: 'fight_id',
            as: 'fight_info'
        }
    },
    {
        $unwind: {
            path: '$fight_info'
        }
    },
    {
        $match: {
            'fight_info.referee': 'Herb Dean'
        }
    },
    {
        $group: {
            _id: '$fight_info.referee',
            avg_ground_time: {
                $avg: '$control'
            }
        }
    }
])
```
![upit3](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit3.png)
*Note: Ovde se na grafu prikazuju rezultati za sve sudije jer nema smisla praviti grafički prikaz za jednog*
![upit3_graph](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit3_graph.png)

- Posle optimizacije: *00:00.045*

```js
db.stats_optimized.aggregate([
    {
        $match: {
            'fight_info.referee': 'Herb Dean'
        }
    },
    {
        $group: {
            _id: '$fight_info.referee',
            avg_ground_time: {
                $avg: '$control'
            }
        }
    }
])
```
![upit3_optimized](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit3_optimized.png)

---

**Pitanje 4**: Koji je odnos pobeda i poraza boraca koje je pobedio Khabib Nurmagomedov?
- Pre optimizacije: *00:14.991*

```js
db.fighters.aggregate([
    {
        $lookup: {
            from: 'fights',
            localField: 'fighter',
            foreignField: 'fighter_name',
            as: 'fights_info'
        }
    },
    {
        $match: {
            'fights_info': {
                $elemMatch: {
                    result: 0,
                    opponent_name: 'khabib nurmagomedov'
                }
            }
        }
    },
    {
        $addFields: {
            "wins": {
                $size: {
                    $filter: {
                        input: "$fights_info",
                        as: "fight",
                        cond: { $eq: ["$$fight.result", 1] }
                    }
                }
            },
            "total_fights": {
                $size: '$fights_info'
            }
        }
    },
    {
        $addFields: {
            "win/loss_ratio": {
                $divide: ["$wins", "$total_fights"]
            }
        }
    },
    {
        $project: {
            fighter: 1,
            wins: 1,
            total_fights: 1,
            'win/loss_ratio': 1
        }
    }
])
```
![upit4](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit4.png)
![upit4_graph](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit4_graph.png)

- Posle optimizacije: *00:00.084*

```js
db.fighters_optimized.aggregate([
    {
        $lookup: {
            from: 'fights',
            localField: 'fighter',
            foreignField: 'fighter_name',
            as: 'fights_info'
        }
    },
    {
        $match: {
            'fights_info': {
                $elemMatch: {
                    result: 0,
                    opponent_name: 'khabib nurmagomedov'
                }
            }
        }
    },
    {
        $addFields: {
            "win/loss_ratio": {
                $divide: ["$wins", "$total_fights"]
            }
        }
    },
    {
        $project: {
            fighter: 1,
            wins: 1,
            total_fights: 1,
            'win/loss_ratio': 1
        }
    }
])
```
![upit4_optimized](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit4_optimized.png)

---

Pitanje 5: Koji je prosečan broj pokušaja rušenja koje su borci imali u borbama u kojima su imali manji reach?
- Pre optimizacije: *02:30.394*

```js
db.fights.aggregate([
    {
        $lookup: {
            from: 'fighters',
            localField: 'fighter_name',
            foreignField: 'fighter',
            as: 'fighter_info'
        }
    },
    {
        $lookup: {
            from: 'fighters',
            localField: 'opponent_name',
            foreignField: 'fighter',
            as: 'opponent_info'
        }
    },
    {
        $unwind: {
            path: '$fighter_info'
        }
    },
    {
        $unwind: {
            path: '$opponent_info'
        }
    },
    {
        $match: {
            "fighter_info.reach": { $exists: true },
            "opponent_info.reach": { $exists: true }
        }
    },
    {
        $lookup: {
            from: 'stats',
            localField: 'fighter_name',
            foreignField: 'fighter_name',
            as: 'stats'
        }
    },
    {
        $unwind: {
            path: '$stats'
        }
    },
    {
        $addFields: {
            reach_advantage: {
                $cond: {
                    if: {
                        $gt: [
                            "$fighter_info.reach",
                            "$opponent_info.reach"
                        ]
                    },
                    then: 'longer',
                    else: 'shorter'
                }
            }
        }
    },
    {
        $match: {
            reach_advantage: 'shorter'
        }
    },
    {
        $group: {
            _id: "$reach_advantage",
            avg_takedowns_attampts: {
                $avg: '$stats.takedowns_attempts'
            }
        }
    }
])
```
![upit5](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit5.png)
*Note: Ovde se prikazuju rezultati i za borce sa dužim reachom jer ne bi imalo smisla prikazivati samo za one sa kraćim*
![upit5_graph](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit5_graph.png)

- Posle optimizacije: *00:00.142*

```js
db.stats_optimized.aggregate([
    {
        $match: {
            reach_advantage: '0'
        }
    },
    {
        $group: {
            _id: "$reach_advantage",
            avg_takedowns_attampts: {
                $avg: '$takedowns_attempts'
            }
        }
    }
])
```
![upit5_optimized](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit5_optimized.png)

---
**Pitanje 6:** Koja su top 3 borca sa najvećim ukupnim borilačkim vremenom u poslednjih 5 godina u light heavyweight diviziji, i koliko je svako od njih ostvario pobeda za to vreme? 
*(00.00.093)*

```js
db.fights.aggregate([
 {
    $match: {
      division: 'Light Heavyweight',
      date: { $gte: new Date(new Date().setFullYear(new Date().getFullYear() - 5)) }
    }
  },
  {
    $sort: {
      fighter_name: 1, 
      date: 1
    }
  },
  {
    $group: {
      _id: '$fighter_name',
      latest_comp_time: { $last: '$total_comp_time' },
      oldest_comp_time: { $first: '$total_comp_time' }
    }
  },
  {
    $addFields: {
      comp_time_last_5_years: { $subtract: ['$latest_comp_time', '$oldest_comp_time'] }
    }
  },
  {
    $sort: {
      comp_time_last_5_years: -1
    }
  },
  {
    $limit: 3
  },
  {
    $lookup: {
      from: 'fights',
      let: { fighter_name: '$_id' },
      pipeline: [
        {
          $match: {
            $expr: {
              $and: [
                { $eq: ['$fighter_name', '$$fighter_name'] },
                { $eq: ['$result', 1] },
                { $gte: ['$date', new Date(new Date().setFullYear(new Date().getFullYear() - 5))] }
              ]
            }
          }
        },
        {
          $count: 'win_count'
        }
      ],
      as: 'win_count'
    }
  },
  {
    $unwind: {
      path: '$win_count',
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $project: {
      _id: 1,
      comp_time_last_5_years: 1,
      win_count: { $ifNull: ['$win_count.win_count', 0] }
    }
  }
  ])

```
![upit6](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit6.png)
![upit6_graph](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit6_graph.png)

---

**Pitanje 7:** Koji borac u bantamweight diviziji ima najveći prosečni broj pokušaja značajnih udaraca po borbi, a da nije izgubio borbu preko jednoglasne odluke? 
- Pre optimizacije: *(01:44)*

```js
db.getCollection("stats").aggregate([
    {
     $lookup: {
       from: 'fights',
       localField: 'fight_id',
       foreignField: 'fight_id',
       as: 'fight_details'
     }
   },
   {
     $unwind: '$fight_details'
   },
   {
     $match: {
       'fight_details.division': 'Bantamweight'
     }
   },
   {
     $group: {
       _id: '$fighter_name',
       avg_sig_strikes_attempts: { $avg: '$sig_strikes_attempts' },
       u_dec_losses: {
         $sum: {
           $cond: [
             { $and: [{ $eq: ['$fight_details.result', 0] }, { $eq: ['$fight_details.method', 'U-DEC'] }] },
             1,
             0
           ]
         }
       }
     }
   },
   {
     $match: {
       u_dec_losses: { $eq: 0 }
     }
   },
   {
     $sort: {
       avg_sig_strikes_attempts: -1
     }
   },
   {
     $limit: 1
   }
 ])
```
![upit7](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit7.png)
![upit7_graph](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit7_graph.png)

- Posle optimizacije: *(00.17s)*

```js
db.getCollection("stats_optimized").aggregate([
    {
      $match: {
        'fight_info.division': 'Bantamweight'
      }
    },
    {
      $group: {
        _id: '$fighter_name',
        avg_sig_strikes_attempts: { $avg: '$sig_strikes_attempts' },
        u_dec_losses: {
          $sum: {
            $cond: [
              { $and: [{ $eq: ['$fight_details.result', 0] }, { $eq: ['$fight_details.method', 'U-DEC'] }] },
              1,
              0
            ]
          }
        }
      }
    },
    {
      $match: {
        u_dec_losses: { $eq: 0 }
      }
    },
    {
      $sort: {
        avg_sig_strikes_attempts: -1
      }
    },
    {
      $limit: 1
    }
  ])
```
![upit7_opt](https://github.com/alexadjukic/SBP-Project/blob/main/images/upit%207%20optimizacija.png)
---

**Pitanje 8:** Koji borac sa ortodox stance-om ima najviše vremena kontrole po borbi, i koliki je njegov procenat uspešnosti u obaranju? 
- Pre optimizacije: *(19:59)*

```js
db.getCollection("stats").aggregate([
    {
      $lookup: {
        from: 'fighters',
        localField: 'fighter_name',
        foreignField: 'fighter',
        as: 'fighter_details'
      }
    },
    {
      $unwind: '$fighter_details'
    },
    {
      $match: {
        'fighter_details.stance': 'Orthodox'
      }
    },
    {
      $group: {
        _id: '$fighter_name',
        total_control_time: { $sum: '$control' },
        fight_count: { $sum: 1 },
        total_takedowns_landed: { $sum: '$takedowns_landed' },
        total_takedowns_attempts: { $sum: '$takedowns_attempts' }
      }
    },
    {
      $project: {
        average_control_time_per_fight: {
          $divide: ['$total_control_time', '$fight_count']
        },
        takedown_accuracy: {
          $cond: {
            if: { $eq: ['$total_takedowns_attempts', 0] },
            then: 0,
            else: {
              $multiply: [
                { $divide: ['$total_takedowns_landed', '$total_takedowns_attempts'] },
                100
              ]
            }
          }
        }
      }
    },
    {
      $sort: {
        average_control_time_per_fight: -1
      }
    },
    {
      $limit: 1
    }
  ]);
```
![upit8](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit8.png)
![upit8_graph](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit8_graph.png)

- Posle optimizacije: *(01.35s)*
```js
db.getCollection("stats_optimized").aggregate([
  {
    $match: {
      'fighter_info.stance': 'Orthodox'
    }
  },
  {
    $group: {
      _id: '$fighter_name',
      total_control_time: { $sum: '$control' },
      fight_count: { $sum: 1 },
      total_takedowns_landed: { $sum: '$takedowns_landed' },
      total_takedowns_attempts: { $sum: '$takedowns_attempts' }
    }
  },
  {
    $project: {
      average_control_time_per_fight: {
        $divide: ['$total_control_time', '$fight_count']
      },
      takedown_accuracy: {
        $cond: {
          if: { $eq: ['$total_takedowns_attempts', 0] },
          then: 0,
          else: {
            $multiply: [
              { $divide: ['$total_takedowns_landed', '$total_takedowns_attempts'] },
              100
            ]
          }
        }
      }
    }
  },
  {
    $sort: {
      average_control_time_per_fight: -1
    }
  },
  {
    $limit: 1
  }
]);
```
![upit8_opt](https://github.com/alexadjukic/SBP-Project/blob/main/images/upit%208%20optimizacija.png)
---
**Pitanje 9:** Izlistati sve informacije o borcima koji su se borili u makar 2 divizije, a tokom karijere imaju procenat realizacije leg strikova preko 60%. 

- Pre optimizacije: *(01:30)*

```js
db.getCollection("stats").aggregate([
    {
      $lookup: {
        from: 'fights',
        localField: 'fight_id',
        foreignField: 'fight_id',
        as: 'fight_details'
      }
    },
    {
      $unwind: '$fight_details'
    },
    {
      $group: {
        _id: '$fighter_name',
        unique_divisions: { $addToSet: '$fight_details.division' },
        leg_strikes_landed: { $sum: '$leg_strikes_landed' },
        leg_strikes_attempts: { $sum: '$leg_strikes_attempts' }
      }
    },
    {
      $match: {
        'unique_divisions.1': { $exists: true },
        $expr: {
          $gt: [
            {
              $cond: {
                if: { $eq: ['$leg_strikes_attempts', 0] },
                then: 0,
                else: { $divide: ['$leg_strikes_landed', '$leg_strikes_attempts'] }
              }
            },
            0.6
          ]
        }
      }
    },
    {
      $lookup: {
        from: 'fighters',
        localField: '_id',
        foreignField: 'fighter',
        as: 'fighter_details'
      }
    },
    {
      $unwind: '$fighter_details'
    },
    {
      $addFields: {
        fighter_details: {
          $mergeObjects: ['$fighter_details', { unique_divisions: '$unique_divisions' }]
        }
      }
    },
    {
      $replaceRoot: {
        newRoot: '$fighter_details'
      }
    }
  ]);
```
![upit9](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit9.png)
![upit9_graph](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit9_graph.png)

- Posle optimizacije: *(01.65s)*

```js
db.getCollection("stats_optimized").aggregate([
    {
      $match: {
        'number_of_divisions': { $gt: 1 },
        $expr: {
          $gt: [
            {
              $cond: {
                if: { $eq: ['$leg_strikes_attempts', 0] },
                then: 0,
                else: { $divide: ['$leg_strikes_landed', '$leg_strikes_attempts'] }
              }
            },
            0.6
          ]
        }
      }
    },
    {
      $lookup: {
        from: 'fighters',
        localField: 'fighter_name',
        foreignField: 'fighter',
        as: 'fighter_details'
      }
    },
    {
      $unwind: '$fighter_details'
    },
    {
      $addFields: {
        fighter_details: {
          $mergeObjects: ['$fighter_details', { unique_divisions: '$number_of_divisions' }]
        }
      }
    },
    {
      $replaceRoot: {
        newRoot: '$fighter_details'
      }
    }
  ]);
```
![upit9_opt](https://github.com/alexadjukic/SBP-Project/blob/main/images/upit%209%20optimizacija.png)
---
**Pitanje 10:** Nađi sve borce koji imaju više od 45 godina, a imali su title fight u toku svoje karijere. 
- Pre optimizacije: *(05:56)*

```js
db.getCollection("fighters").aggregate([
  {
    $addFields: {
      age_now: {
        $divide: [
          { $subtract: [new Date(), "$dob"] },
          1000 * 60 * 60 * 24 * 365
        ]
      }
    }
  },
  {
    $match: {
      age_now: { $gt: 45 }
    }
  },
  {
    $lookup: {
      from: "stats",
      localField: "fighter",
      foreignField: "fighter_name",
      as: "title_fights"
    }
  },
  {
    $match: {
      "title_fights.title_fight": 1
    }
  },
  {
    $project: {
      _id: 0,
      fighter: 1
    }
  }
]);
```
![upit10](https://github.com/alexadjukic/SBP-Project/blob/main/images/Upit10.png)

-Posle optimizacije: *(00.102s)*

```js
db.getCollection("fighters_optimized").aggregate([
  {
    $addFields: {
      age_now: {
        $divide: [
          { $subtract: [new Date(), "$dob"] },
          1000 * 60 * 60 * 24 * 365
        ]
      }
    }
  },
  {
    $match: {
      age_now: { $gt: 45 }
    }
  },
  {
    $match: {
      "had_title_fight": true
    }
  },
  {
    $project: {
      _id: 0,
      fighter: 1
    }
  }
]);
```
![upit10_opt](https://github.com/alexadjukic/SBP-Project/blob/main/images/upit%2010%20optimizacija.png)

---
![performance](https://github.com/alexadjukic/SBP-Project/blob/main/images/poredjenje%20performansi.png)
