
from datetime import datetime
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app=Flask(__name__)

db=SQLAlchemy(app)
ms=Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:@localhost/feedback"


#MODEL FOR FEEDBACK

class Feedback(db.Model):
    ID=db.Column(db.Integer, primary_key= True)
    Name=db.Column(db.String(30), nullable=False)
    Feedback=db.Column(db.String(100), nullable=True) 
    Time =db.Column(db.DateTime, default=datetime.utcnow, nullable=True) 

    def __init__(self,ID,Name,Feedback,Time):
        self.ID=ID
        self.Name=Name
        self.Feedback=Feedback
        self.Time=Time

#SCHEMA FOR FEEDBACK

class FeedbackSchema (ms.Schema):
    class Meta:
        fields= ('ID', 'Name', 'Feedback', 'Uploaded_Time')

#schema object for post
feedbackSchema=FeedbackSchema()
feedbacksSchema=FeedbackSchema(many= True)

@app.route("/addFeedback", methods=['POST'])
def addFeedback():
    
    feedbackMetaData=request.json["feedbackMetaData"]
    newFeedback= Feedback(feedbackMetaData["ID"], feedbackMetaData["Name"], feedbackMetaData["Feedback"], 
                            feedbackMetaData["Time"] )
    db.session.add(newFeedback)
    db.session.commit()
    return jsonify({"Action is successful": "200 OK"}),200   
       

@app.route("/delete/<int:ID>", methods=["DELETE"])
def deletePost(ID):
    feedback= Feedback.query.get(ID)
    db.session.delete(feedback)
    db.session.commit()
    return jsonify({"Action is successful": "200 OK"}),200

@app.route("/update/<int:ID>", methods=["PUT","GET"])
def updatePost(ID):
    feedbackMetaData=request.json["feedbackMetaData"]

    feedback= Feedback.query.get(ID)
    feedback.ID= feedbackMetaData["ID"]
    feedback.Name= feedbackMetaData["Name"]
    feedback.Feedback= feedbackMetaData["Feedback"]

    db.session.commit()
    return jsonify({"Action is successful": "200 OK"}),200

@app.route("/feedbacks", methods=['GET'])
@app.route("/feedbacks/<int:ID>", methods=['GET'])
def viewPost(ID=0):
    if ID==0:
        feedbacks= Feedback.query.all()
        allfeedbacks= feedbacksSchema.dump(feedbacks)
        return jsonify(allfeedbacks)
    else:
        feedback= Feedback.query.get(ID)
        return feedbackSchema.jsonify(feedback)    


if __name__=="__main__":
    app.run( debug= True)