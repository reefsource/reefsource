import {Upload} from './upload';

export interface Album {
  id?: number,
  created?: Date,
  modified?: Date,
  name: string,
  lat: number,
  lng: number,
  date: Date,
  upload_count?: number
  uploads?: Array<Upload>
}
