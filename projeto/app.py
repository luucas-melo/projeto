from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


@app.route('/')
def dados():
   return render_template('index.html',title='Dados')

@app.route('/form/')
def form():
	return render_template('form.html',title='Qual o seu privilégio')
	 				
@app.route('/form/result',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form
		url = 'https://raw.githubusercontent.com/twistershark/ds-grupo-Whyskritorio/master/pnad2012.csv'
		df = pd.read_csv(url, index_col=0)
		df2 = df.fillna(0) #zerando os nan
		df3 = df2.copy()
		df3[['income', 'income_work', 'income_rent', 'income_capital']] = df2[['income','income_work','income_rent','income_capital']].multiply(1.4907)
		brancos = df3[(df3.race == 16) | (df3.race == 1)]
		negros = df3[(df3.race == 2) | (df3.race == 4) | (df.race == 8)]
		nome = request.form['nome']
		#brancos e negros	
		media = float(df['income'].mean())
		renda = float(request.form['renda'])
		valor = round(renda-media,2) 
		md_bran = float((brancos.income * brancos.weight).sum() / brancos.weight.sum())
		md_negr = float((negros.income * negros.weight).sum() / negros.weight.sum())
		valor_bran = round(renda-md_bran,2)  
		valor_negr = round(renda-md_negr,2)	 
		#homens e mulheres
		md_genero = df3[df3.income>0].groupby('gender').mean() #1= masculino; 2=feminino
		md_homem = float(md_genero.income[1])
		renda_homem = round(renda-md_homem,2)
		md_mulher = float(md_genero.income[2])
		renda_mulher = round(renda-md_mulher,2)
		return render_template("result.html",result = result, valor = valor,media=media,renda=renda, nome=nome,valor_bran=valor_bran,valor_negr=valor_negr,renda_homem=renda_homem,renda_mulher=renda_mulher)
  
     

@app.route('/pnad/')
def pnad():
	url = 'https://raw.githubusercontent.com/twistershark/ds-grupo-Whyskritorio/master/pnad2012.csv'
	df = pd.read_csv(url, index_col=0)
	df2 = df.fillna(0) #zerando os nan
	df3 = df2.copy()
	df3[['income', 'income_work', 'income_rent', 'income_capital']] = df2[['income','income_work','income_rent','income_capital']].multiply(1.4907)
	return render_template("pnad.html", column_names=df3.columns.values, row_data=list(df3.head(100).values.tolist()),
						link_column="teste", zip=zip,title='Qual o seu privilégio')
if __name__ == '__main__':
	app.run(debug = True)
   

