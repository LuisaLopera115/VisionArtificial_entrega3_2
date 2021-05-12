using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveCam : MonoBehaviour
{
    public GameObject Avion;
    //Transform cam;
    Vector3 pos;
    void Start()
    {
        pos = transform.position;
        //cam = gameObject.GetComponent<Transform>();
    }

    // Update is called once per frame
    void Update()
    {
        
        //transform.position = new Vector3(Avion.transform.position.x + ofsetx, Avion.transform.position.y + ofsety, Avion.transform.position.z + ofsetz);
        transform.position = new Vector3(pos.x, pos.y, Avion.transform.position.z);
    }
}
