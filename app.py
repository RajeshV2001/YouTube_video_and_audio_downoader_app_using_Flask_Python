from flask import Flask,render_template,request
import pytube as yt
import easygui
import os


app=Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/music_download',methods=["GET","POST"])
def music():
    
    
    if request.method=='POST':
        try:
    
            url=request.form['url']
            
            stream=yt.YouTube(url)
            
            audio=stream.streams.filter(only_audio=True).first()
            
            size=audio.filesize_mb
            path=easygui.diropenbox()
            
            file=audio.download(output_path=path)
            
            base,ext=os.path.splitext(file)
            name=base+"music"+".mp3"
            os.rename(file,name)
            
            return render_template("download.html",size=size,res="")
        except:
            return render_template("download.html",error="Invalid URL or Network ERROR")
            
            
    else:
        return render_template("music.html")
    
    
    
    
    
@app.route('/get',methods=["GET","POST"])
def get():
    
    if request.method=="POST":
        
        try:
            
        
            url=request.form['url']
            pt=yt.YouTube(url)
            video=pt.streams.filter(progressive=True).desc()
            lst=[i.resolution for i in video]
            lst=list(set(lst))
            
            return render_template("video_confirm.html",url=url,lst=lst)
        
        except:
            return render_template("download.html",error="Invalid URL or Network ERROR")
            
    
    else:
        return render_template("video.html")
        
   

@app.route('/video_download',methods=["GET","POST"])
def video():
    
    if request.method=="POST":
        
        try:
            url=request.form['url']
            res=request.form['select']

            pt=yt.YouTube(url)
            video=pt.streams.filter(res=res,progressive=True).first()
            
            size=video.filesize_mb
            path=easygui.diropenbox()
            video.download(output_path=path)
            
            return render_template("download.html",size=size,res=res)
        
        except:
            
            return render_template("download.html",error="Invalid URL or Network ERROR")
    else:
        
        return render_template('video.html')


    
    

if __name__=='__main__':
    app.run(debug=False)