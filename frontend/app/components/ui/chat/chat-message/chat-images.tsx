import Image from "next/image";
import { ImagesData, type ImageData } from "../index";
import { Fragment, useState } from "react";
import { Button } from "../../button";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "../../drawer";

export function ChatImages({ data }: { data: ImagesData }) {
  // console.log("=========")
  const [zoomedImage, setZoomedImage] = useState(null);
  const openZoomedImage = (imageUrl:any) => {
    setZoomedImage(imageUrl);
  };  
  const closeZoomedImage = () => {
    setZoomedImage(null);
  };

  const image_list = 
    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mx-5">
    {
      data.map((link, index)=>{
        // console.log("==>", link)
        return (
          <div className="rounded-md max-w-[500px] shadow-md my-2" key={index} onClick={() => openZoomedImage(link.url)}>
            <p><b>{link.desc}</b></p>
            <Image
              src={link.url}
              width={0}
              height={0}
              sizes="100vw"
              style={{ width: "100%", height: "auto" }}
              alt={link.desc}
            />
          </div>
        )
      })        
    }
    </div>
  return (
      <div className="flex flex-col space-y-2">
        <strong>[[참고 이미지]]</strong>
      {(image_list)}
      {/* Render the zoomed image */}
      {zoomedImage && (
        <div className="zoomed-image-container" onClick={closeZoomedImage}>
          <Image src={zoomedImage} alt="zoomed-image" layout="fill" objectFit="contain" />
        </div>
      )}        
      </div>

  );
}
