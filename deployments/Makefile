.PHONY: deploy-dev deploy-prod clean

deploy-dev:
	kubectl kustomize overlays/dev | kubectl apply -f - --validate=false

deploy-prod:
	kubectl kustomize overlays/prod | kubectl apply -f -

clean:
	kubectl kustomize overlays/dev | kubectl delete -f - || true
	kubectl delete namespace schedule-queue-system || true