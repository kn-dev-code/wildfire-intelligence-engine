FROM node:22-alpine

WORKDIR /code

COPY package.json ./ package-lock.json ./

RUN npm install
RUN npm run build -- --mode frontend
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]