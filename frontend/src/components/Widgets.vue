<!--  Functional components that determines the widget to be displayed
      Based on the type of field
-->

<template functional>
  <div>
    <div v-if="props.field.dataType === 'integer'" class="form-group" >
      <label :for="props.field.name">{{ props.field.name }}</label>
      <input :value="props.field.value" type="number" class="form-control" />
    </div>

    <div v-else-if="props.field.dataType === 'currency'" class="form-group">
      <label for="props.field.name">{{ props.field.name }}</label>
      <div class="input-group mb-2">
        <div class="input-group-prepend">
          <div class="input-group-text">$</div>
        </div>
        <input :value="props.field.value" type="number" class="form-control">
      </div>
    </div>

    <div v-else-if="props.field.dataType === 'date'" class="form-group" >
      <label :for="props.field.name">{{ props.field.name }}</label>
      <input :value="props.field.value" type="date" class="form-control" />
    </div>

    <div v-else-if="props.field.dataType === 'enum'" class="form-group">
      <label :for="props.field.name">{{ props.field.name }}</label>
      <select class="form-control">
        <option :selected="option === props.field.value" :key="option" v-for="option in props.field.options">
          {{ option }}
        </option>
      </select>
    </div>

    <div v-else class="form-group">
      <label :for="props.field.name">{{ props.field.name }}</label>
      <input :value="props.field.value" class="form-control" type="text" />
    </div>
  </div>
</template>
