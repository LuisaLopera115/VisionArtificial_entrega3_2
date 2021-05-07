using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveCam : MonoBehaviour
{
    public GameObject Avion;
    private Transform cam;
    float ofsetx = -857;
    float ofsety = 375;
    float ofsetz = 5;
    void Start()
    {
        //cam = gameObject.GetComponent<Transform>();
    }

    // Update is called once per frame
    void Update()
    {
        transform.position = new Vector3(Avion.transform.position.x + ofsetx, Avion.transform.position.y + ofsety, Avion.transform.position.z + ofsetz);
    }
}
