import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {ActivatedRoute, Params} from '@angular/router';
import {Store} from '@ngrx/store';
import * as fromRoot from '../../reducers';
import {FileUploader} from 'ng2-file-upload';
import {CookieService} from 'ngx-cookie';
import {MdSnackBar} from '@angular/material';
@Component({
  selector: 'app-uploader',
  templateUrl: './uploader.component.html',
  styleUrls: ['./uploader.component.css']
})
export class UploaderComponent implements OnInit {

  public albumId: number;
  public uploader: FileUploader;

  @Output() itemComplete: EventEmitter<any> = new EventEmitter();

  constructor(private route: ActivatedRoute,
              private store: Store<fromRoot.State>,
              private _cookieService: CookieService,
              public snackBar: MdSnackBar) {

  }

  openSnackBar(message: string, action?: string) {
    this.snackBar.open(message, action, {
      duration: 2000,
    });
  }

  ngOnInit() {
    this.route.params
      .subscribe((params: Params) => {
        this.albumId = +params['albumId'];
        this.uploader = new FileUploader({url: `/api/v1/albums/${this.albumId}/upload/`});
        this.uploader.setOptions({
          headers: [{name: 'X-CSRFToken', value: this._cookieService.get('csrftoken')}],
          filters: [{
            name: 'only_raw', fn: (item, options) => item.name.toLowerCase().endsWith('.gpr')
          }]
        });
        this.uploader.onCompleteAll = () => {
          this.itemComplete.emit();
        };
        this.uploader.onWhenAddingFileFailed = (item, filter, options) => {
          this.openSnackBar('Only GoPro RAW files (.GPR) can be uploaded');
        }
      });
  }
}
