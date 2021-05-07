using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Generator : MonoBehaviour
{
    [SerializeField] GameObject[] tiles;
    public float Timer = 2;
    int i = 0;
    void Start()
    {
        i = Random.Range(0, tiles.Length - 1);
        InvokeRepeating("CreateObstacle", Timer, Timer);
    }

    
    void Update()
    {
        i = Random.Range(0, tiles.Length - 1);
    }
    void CreateObstacle()
    {
        Instantiate(tiles[i], transform.position, Quaternion.identity);
    }
}
