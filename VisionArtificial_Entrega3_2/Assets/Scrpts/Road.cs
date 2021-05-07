using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Road : MonoBehaviour
{
    private int selectedTile;
    public GameObject[] tiles;
    public Transform plane;
    private float nexttilex = 0;
    void Start()
    {
        selectedTile = Random.Range(0,tiles.Length-1);
    }

    void Update()
    {
        if (plane.position.x > nexttilex)
        {
            nexttilex += 11600;
            GameObject tempRoad =  GameObject.Instantiate(tiles[selectedTile]);
            tempRoad.GetComponent<Transform>().position = new Vector3(nexttilex, -400,0);
            selectedTile = Random.Range(0, tiles.Length - 1);
        }
    }
}
