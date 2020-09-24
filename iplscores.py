from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import SelectField,FloatField,IntegerField,SubmitField
from wtforms.validators import DataRequired
import pickle

app=Flask(__name__)

app.config['SECRET_KEY']='somekey'

class IplFormClass(FlaskForm):
    Num_of_overs = FloatField('Enter Number of overs completed till now',validators=[DataRequired()])
    Runs = IntegerField('Runs scored in last 5 overs',validators=[DataRequired()])
    Wickets = IntegerField('Wickets in last 5 overs',validators=[DataRequired()])
    Batting_Team = SelectField('BattingTeam',
                               choices=(('KKR','KKR'),('CSK','CSK'),('MI','MI'),('RR','RR'),('DC','DC'),('KXIP','KXIP'),('SRH','SRH'),('RCB','RCB')),validators=[DataRequired()])
    Bowling_Team = SelectField('BowlingTeam',
                               choices=(('KKR','KKR'),('CSK','CSK'),('MI','MI'),('RR','RR'),('DC','DC'),('KXIP','KXIP'),('SRH','SRH'),('RCB','RCB')),validators=[DataRequired()])
    Submit = SubmitField()



@app.route('/predict',methods=['GET','POST'])
def predict_totalscore():
    form = IplFormClass()
    if form.validate_on_submit():
        Overs=form.Num_of_overs.data
        Runs=form.Runs.data
        Wickets=form.Wickets.data
        if form.Batting_Team.data=='CSK':
            Bat=[0,0,0,0,0,0,0]
        elif form.Batting_Team.data=='DC':
            Bat=[1,0,0,0,0,0,0]
        elif form.Batting_Team.data=='KXIP':
            Bat=[0,1,0,0,0,0,0]
        elif form.Batting_Team.data=='KKR':
            Bat=[0,0,1,0,0,0,0]
        elif form.Batting_Team.data=='MI':
            Bat=[0,0,0,1,0,0,0]
        elif form.Batting_Team.data=='RR':
            Bat=[0,0,0,0,1,0,0]
        elif form.Batting_Team.data=='RCB':
            Bat=[0,0,0,0,0,1,0]
        elif form.Batting_Team.data=='SRH':
            Bat=[0,0,0,0,0,0,1]
        if form.Bowling_Team.data=='CSK':
            Bowl=[0,0,0,0,0,0,0]
        elif form.Bowling_Team.data=='DC':
            Bowl=[1,0,0,0,0,0,0]
        elif form.Bowling_Team.data=='KXIP':
            Bowl=[0,1,0,0,0,0,0]
        elif form.Bowling_Team.data=='KKR':
            Bowl=[0,0,1,0,0,0,0]
        elif form.Bowling_Team.data=='MI':
            Bowl=[0,0,0,1,0,0,0]
        elif form.Bowling_Team.data=='RR':
            Bowl=[0,0,0,0,1,0,0]
        elif form.Bowling_Team.data=='RCB':
            Bowl=[0,0,0,0,0,1,0]
        elif form.Bowling_Team.data=='SRH':
            Bowl=[0,0,0,0,0,0,1]
        ipl_pkl_model=pickle.load(open('iplfile.pkl','rb'))
        ipl_input=[Overs]+[Runs]+[Wickets]+Bat+Bowl
        predict=ipl_pkl_model.predict([ipl_input])
        print('predict')
        return render_template('predictions.html',predict=predict,form=form)
    return render_template('predictions.html',form=form)

if __name__=='__main__':
    app.run(debug=True)