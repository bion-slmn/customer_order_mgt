minikube start:
	minikube start --driver=docker

make_docker-image:
	docker build -t django-web:latest .

deploy:
	kubectl apply -f k8s/django-deployment.yaml
	kubectl apply -f k8s/rqworker-deployment.yaml
	kubectl apply -f k8s/rqworker-service.yaml
	kubectl apply -f k8s/redis-deployment.yaml
	

delete-all-pods:
	kubectl delete pods --all

deploy_migration:
	kubectl exec -it $(POD_NAME) -- python manage.py migrate

port-forward:
	kubectl port-forward service/django-web 8000:8000

