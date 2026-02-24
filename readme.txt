#Lembre-se de atualizar .env para o banco principal;

#É necessário ter o Docker aberto durante o processo;

#Lembre-se de colocar shutdown_vm() em generate_pdf_with_reportlab.py fora de um comentário;

#autenticar no glcoud:
gcloud auth login

#selecionar projeto
gcloud config set project msenaval-453016

#verficar se funcionou
gcloud auth list

#criar imagem no docker
docker build -t gcr.io/msenaval-453016/pdf-generator:latest .

#testar imagem:
docker run -p 8080:8080 gcr.io/msenaval-453016/pdf-generator:latest

#envio da imagem para o cloud container
gcloud auth configure-docker
docker push gcr.io/msenaval-453016/pdf-generator:latest