using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Clouds : MonoBehaviour
{
    Transform Cloud;
    float move;
    float speed = 100f;
    void Start()
    {
        Cloud = GetComponent<Transform>();
        move = Random.Range(-1, 2);
    }

    // Update is called once per frame
    void Update()
    {
        Cloud.position += new Vector3(0,0,move)*Time.deltaTime*speed;
        move = Random.Range(-1, 1);
    }
}
