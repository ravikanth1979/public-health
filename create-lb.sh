# Copyright Google Inc. 2017
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

export BACKEND_PORT=30033

echo "Creating firewall rules..."
gcloud compute firewall-rules create gke-public-health-dashboard-lb7-fw --target-tags public-health-dashboard-node --allow "tcp:${BACKEND_PORT}" --source-ranges 130.211.0.0/22,35.191.0.0/16

echo "Creating health checks..."
gcloud compute health-checks create http public-health-dashboard-basic-check --port $BACKEND_PORT --healthy-threshold 1 --unhealthy-threshold 10 --check-interval 60 --timeout 60

echo "Creating an instance group..."
export INSTANCE_GROUP=$(gcloud container clusters describe public-health-dashboard-cluster --format="value(instanceGroupUrls)" | awk -F/ '{print $NF}')

echo "Creating named ports..."
gcloud compute instance-groups managed set-named-ports $INSTANCE_GROUP --named-ports "port${BACKEND_PORT}:${BACKEND_PORT}"

echo "Creating the backend service..."
gcloud compute backend-services create public-health-dashboard-service --protocol HTTP --health-checks public-health-dashboard-basic-check --port-name "port${BACKEND_PORT}" --global

echo "Connecting instance group to backend service..."
export INSTANCE_GROUP_ZONE=$(gcloud config get-value compute/zone)
gcloud compute backend-services add-backendpublic-health-dashboard-service --instance-group $INSTANCE_GROUP --instance-group-zone $INSTANCE_GROUP_ZONE --global

echo "Creating URL map..."
gcloud compute url-maps create public-health-dashboard-urlmap --default-service public-health-dashboard-service

echo "Uploading SSL certificates..."
gcloud compute ssl-certificates create public-health-dashboard-ssl-cert --certificate /tmp/public-health-dashboard-ssl/ssl.crt --private-key /tmp/public-health-dashboard-ssl/ssl.key

echo "Creating HTTPS target proxy..."
gcloud compute target-https-proxies create public-health-dashboard-https-proxy --url-map public-health-dashboard-urlmap --ssl-certificates public-health-dashboard-ssl-cert

echo "Creating global forwarding rule..."
gcloud compute forwarding-rules create public-health-dashboard-gfr --address $STATIC_IP --global --target-https-proxypublic-health-dashboard-https-proxy --ports 443
